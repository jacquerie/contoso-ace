# -*- coding: utf-8 -*-

from datetime import datetime

from fbmessenger import MessengerClient
from flask import Blueprint, current_app, jsonify, render_template, request
from flask_login import current_user, login_required, login_user, logout_user

from .models import Chat, Customer, Employee, Entity, Message, db

DAY = 24 * 60 * 60 * 1000

app = Blueprint('app', __name__)


class EntityModel:
    def predict(self, text):
        return [
            {
                'snippet': 'Paris',
                'type': 'LOC',
            },
            {
                'snippet': 'next Monday',
                'type': 'DATE',
            },
            {
                'snippet': '1:30 local time',
                'type': 'TIME',
            },
        ]


class IntentModel:
    def predict(self, text):
        return 'CAR RENTAL'


@app.route('/', methods=['GET'])
@app.route('/<path:path>', methods=['GET'])
def root(path=None):
    return render_template('index.html'), 200


@app.route('/webhook', methods=['GET'])
def webhook_get():
    facebook_verify_token = current_app.config['FACEBOOK_VERIFY_TOKEN']

    if request.args.get('hub.mode') == 'subscribe':
        if request.args.get('hub.verify_token') == facebook_verify_token:
            return request.args.get('hub.challenge'), 200
    return 'KO', 403


@app.route('/webhook', methods=['POST'])
def webhook_post():
    facebook_page_token = current_app.config['FACEBOOK_PAGE_TOKEN']
    messenger_client = MessengerClient(facebook_page_token)

    event_data = request.get_json(force=True)

    for entry in event_data['entry']:
        for message in entry['messaging']:
            if message.get('message'):
                facebook_id = message['sender']['id']
                customer = Customer.get_customer_by_facebook_id(facebook_id)
                if not customer:
                    customer_data = messenger_client.get_user_data(message)
                    customer = Customer(
                        facebook_id=facebook_id,
                        first_name=customer_data['first_name'],
                        full_name='{} {}'.format(
                            customer_data['first_name'],
                            customer_data['last_name'],
                        )
                    )
                    db.session.add(customer)
                    db.session.commit()

                timestamp = message['timestamp']
                if customer.chats and customer.chats[-1].last_timestamp - timestamp < DAY:
                    chat = customer.chats[-1]
                    chat.last_timestamp = timestamp
                else:
                    chat = Chat(
                        customer_id=customer.id,
                        last_timestamp=timestamp,
                    )
                db.session.add(chat)
                db.session.commit()

                text = message['message'].get('text', '')
                message = Message(
                    chat_id=chat.id,
                    sender='customer',
                    text=text,
                    timestamp=timestamp,
                )
                db.session.add(message)
                db.session.commit()

    return 'OK', 200


@app.route('/api/chats', methods=['GET'])
@login_required
def api_chats():
    chats = Chat.get_unassigned_chats()

    return jsonify([
        {
            '_id': chat.id,
            'customer': {
                '_id': chat.customer.id,
                'full_name': chat.customer.full_name,
            },
            'message': {
                '_id': chat.messages[0].id,
                'text': chat.messages[0].text,
                'timestamp': chat.messages[0].timestamp,
            },
        } for chat in chats
    ]), 200


@app.route('/api/chats/<int:chat_id>', methods=['GET'])
@login_required
def api_chat_by_id(chat_id):
    chat = Chat.get_chat_by_id(chat_id)
    if current_user.id != chat.employee_id:
        return jsonify({'success': False}), 403

    return jsonify({
        '_id': chat.id,
        'customer': {
            '_id': chat.customer.id,
            'first_name': chat.customer.first_name,
            'full_name': chat.customer.full_name,
        },
        'entities': [
            {
                '_id': entity.id,
                'snippet': entity.snippet,
                'type': entity.type,
            } for entity in chat.entities
        ],
        'intent': chat.intent,
        'messages': [
            {
                '_id': message.id,
                'sender': message.sender,
                'text': message.text,
                'timestamp': message.timestamp,
            } for message in chat.messages
        ],
    }), 200


@app.route('/api/chats/<int:chat_id>/employees', methods=['POST'])
@login_required
def api_chat_add_employee(chat_id):
    chat = Chat.get_chat_by_id(chat_id)
    if chat.employee_id:
        return jsonify({'success': False}), 403

    chat.employee_id = current_user.id
    db.session.add(chat)
    db.session.commit()

    return jsonify({'success': True}), 200


@app.route('/api/chats/<int:chat_id>/entities', methods=['POST'])
@login_required
def api_chat_add_entity(chat_id):
    chat = Chat.get_chat_by_id(chat_id)
    if current_user.id != chat.employee_id:
        return jsonify({'success': False}), 403

    entity_data = request.get_json(force=True)

    entity = Entity(
        chat_id=chat_id,
        snippet=entity_data['snippet'],
        type=entity_data['type'],
    )
    db.session.add(entity)
    db.session.commit()

    return jsonify({
        '_id': entity.id,
        'chat_id': entity.chat_id,
        'snippet': entity.snippet,
        'type': entity.type,
    }), 200


@app.route('/api/chats/<int:chat_id>/messages', methods=['POST'])
@login_required
def api_chat_add_message(chat_id):
    chat = Chat.get_chat_by_id(chat_id)
    if current_user.id != chat.employee_id:
        return jsonify({'success': False}), 403

    message_data = request.get_json(force=True)
    if not message_data['text']:
        return jsonify({'success': False}), 422

    facebook_page_token = current_app.config['FACEBOOK_PAGE_TOKEN']
    messenger_client = MessengerClient(facebook_page_token)
    messenger_client.send(
        {'text': message_data['text']},
        {'sender': {'id': chat.customer.facebook_id}},
        'RESPONSE',
    )

    message = Message(
        chat_id=chat_id,
        sender='employee',
        text=message_data['text'],
        timestamp=int(datetime.now().timestamp() * 1000)
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({
        '_id': message.id,
        'chat_id': message.chat_id,
        'sender': 'employee',
        'text': message.text,
        'timestamp': message.timestamp,
    }), 200


@app.route('/api/chats/<int:chat_id>/predict', methods=['POST'])
@login_required
def api_chat_predict(chat_id):
    chat = Chat.get_chat_by_id(chat_id)
    if current_user.id != chat.employee_id:
        return jsonify({'success': False}), 403

    entity_model = EntityModel()
    intent_model = IntentModel()

    text = '\n'.join(
        message.text for message in chat.messages if message.sender == 'customer')
    entities = entity_model.predict(text)
    intent = intent_model.predict(text)

    for entity in chat.entities:
        db.session.delete(entity)
    db.session.add_all([
        Entity(
            chat_id=chat_id,
            snippet=entity['snippet'],
            type=entity['type'],
        ) for entity in entities
    ])
    chat.intent = intent
    db.session.add(chat)
    db.session.commit()

    return jsonify({
        '_id': chat.id,
        'entities': [
            {
                '_id': entity.id,
                'snippet': entity.snippet,
                'type': entity.type,
            } for entity in chat.entities
        ],
        'intent': chat.intent,
    }), 200


@app.route('/api/employees/current', methods=['GET'])
@login_required
def api_employees_current():
    return jsonify({
        '_id': current_user.id,
        'email': current_user.email,
        'first_name': current_user.first_name,
    }), 200


@app.route('/api/employees/login', methods=['POST'])
def api_employees_login():
    employee_data = request.get_json(force=True)

    employee = Employee.get_employee_by_email_and_password(
        email=employee_data['email'], password=employee_data['password'])

    if employee:
        login_user(employee)
        return jsonify({'success': True}), 200
    return jsonify({'success': False}), 403


@app.route('/api/employees/logout', methods=['POST'])
@login_required
def api_employees_logout():
    logout_user()
    return jsonify({'success': True}), 200
