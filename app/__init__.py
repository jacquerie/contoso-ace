# -*- coding: utf-8 -*-

import os
from datetime import datetime

from fbmessenger import MessengerClient
from flask import Flask, current_app, jsonify, render_template, request
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_sqlalchemy import SQLAlchemy

DAY = 24 * 60 * 60 * 1000


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    FACEBOOK_PAGE_TOKEN = os.getenv('FACEBOOK_PAGE_TOKEN')
    FACEBOOK_VERIFY_TOKEN = os.getenv('FACEBOOK_VERIFY_TOKEN')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__, template_folder='static')
app.config.from_object(Config)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
lm = LoginManager(app)


@lm.user_loader
def load_employee(employee_id):
    return Employee.get_employee_by_id(int(employee_id))


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html'), 200


@app.route('/webhook', methods=['GET'])
def webhook_get():
    facebook_verify_token = current_app.config['FACEBOOK_VERIFY_TOKEN']

    if request.args.get('hub.mode') == 'subscribe':
        if request.args.get('hub.verify_token') == facebook_verify_token:
            return request.args.get('hub.challenge'), 200
    return 'FACEBOOK_VERIFY_TOKEN does not match', 403


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
        'messages': [
            {
                '_id': message.id,
                'text': message.text,
                'timestamp': message.timestamp,
            } for message in chat.messages
        ],
    }), 200


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

    facebook_page_token = current_app.config['FACEBOOK_PAGE_TOKEN']
    messenger_client = MessengerClient(facebook_page_token)
    messenger_client.send(
        {'text': message_data['text']},
        {'sender': {'id': chat.customer.facebook_id}},
        'RESPONSE',
    )

    message = Message(
        chat_id=chat_id,
        text=message_data['text'],
        timestamp=int(datetime.now().timestamp() * 1000)
    )
    db.session.add(message)
    db.session.commit()

    return jsonify({
        '_id': message.id,
        'chat_id': message.chat_id,
        'text': message.text,
        'timestamp': message.timestamp,
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


class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(
        db.Integer(), db.ForeignKey('chat.id'), nullable=False)
    sender = db.Column(
        db.Enum('customer', 'employee', name='sender_enum'), nullable=False)
    text = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.BigInteger(), nullable=False)


class Entity(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(
        db.Integer(), db.ForeignKey('chat.id'), nullable=False)
    snippet = db.Column(db.String(), nullable=False)
    type = db.Column(
        db.Enum('DATE', 'LOC', 'TIME', name='type_enum'), nullable=False)


class Chat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    customer_id = db.Column(
        db.Integer(), db.ForeignKey('customer.id'), nullable=False)
    employee_id = db.Column(
        db.Integer(), db.ForeignKey('employee.id'))
    last_timestamp = db.Column(db.BigInteger(), nullable=False)
    entities = db.relationship(
        'Entity', backref='chat', lazy='selectin', order_by=Entity.id)
    messages = db.relationship(
        'Message', backref='chat', lazy='selectin',
        order_by=Message.timestamp)

    @staticmethod
    def get_chat_by_id(chat_id):
        return Chat.query.filter(Chat.id == chat_id).one_or_none()

    @staticmethod
    def get_unassigned_chats():
        return Chat.query.filter(Chat.employee_id.is_(None))\
            .order_by(Chat.last_timestamp.desc()).limit(10).all()


class Customer(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    facebook_id = db.Column(db.String(), unique=True)
    first_name = db.Column(db.String(), nullable=False)
    full_name = db.Column(db.String(), nullable=False)
    chats = db.relationship(
        'Chat', backref='customer', lazy='selectin',
        order_by=Chat.last_timestamp)

    @staticmethod
    def get_customer_by_facebook_id(facebook_id):
        return Customer.query.filter(Customer.facebook_id == facebook_id).one_or_none()


class Employee(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    chats = db.relationship(
        'Chat', backref='employee', lazy='selectin',
        order_by=Chat.last_timestamp)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf8')

    @staticmethod
    def get_employee_by_email_and_password(email, password):
        employee = Employee.query.filter(Employee.email == email).one_or_none()
        if employee and bcrypt.check_password_hash(employee.password, password):
            return employee

    @staticmethod
    def get_employee_by_id(employee_id):
        return Employee.query.filter(Employee.id == employee_id).one_or_none()
