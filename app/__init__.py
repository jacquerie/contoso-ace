# -*- coding: utf-8 -*-

import os

from fbmessenger import BaseMessenger
from flask import Flask, current_app, jsonify, render_template, request
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

DAY = 24 * 60 * 60 * 1000


class Messenger(BaseMessenger):
    def __init__(self, page_access_token):
        self.page_access_token = page_access_token
        super(Messenger, self).__init__(self.page_access_token)

    def account_linking(self, message):
        pass  # pragma: nocover

    def delivery(self, message):
        pass  # pragma: nocover

    def message(self, message):
        facebook_id = self.get_user_id()
        customer = Customer.get_customer_by_facebook_id(facebook_id)
        if not customer:
            customer_data = self.get_user()
            customer = Customer(
                facebook_id=facebook_id,
                first_name=customer_data['first_name'],
                full_name='{} {}'.format(
                    customer_data['first_name'],
                    customer_data['last_name'],
                ),
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

    def optin(self, message):
        pass  # pragma: nocover

    def postback(self, message):
        pass  # pragma: nocover

    def read(self, message):
        pass  # pragma: nocover


class Config:
    FACEBOOK_PAGE_TOKEN = os.getenv('FACEBOOK_PAGE_TOKEN')
    FACEBOOK_VERIFY_TOKEN = os.getenv('FACEBOOK_VERIFY_TOKEN')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__, template_folder='static')
app.config.from_object(Config)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)


@app.route('/', methods=['GET'])
def root():
    return render_template('index.html'), 200


@app.route('/webhook', methods=['GET'])
def webhook_get():
    facebook_verify_token = current_app.config['FACEBOOK_VERIFY_TOKEN']
    if request.args.get('hub.verify_token') == facebook_verify_token:
        return request.args.get('hub.challenge'), 200
    return 'FACEBOOK_VERIFY_TOKEN does not match', 403


@app.route('/webhook', methods=['POST'])
def webhook_post():
    facebook_page_token = current_app.config['FACEBOOK_PAGE_TOKEN']
    messenger = Messenger(facebook_page_token)
    messenger.handle(request.get_json(force=True))
    return 'OK', 200


@app.route('/api/chats', methods=['GET'])
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
def api_chat_by_id(chat_id):
    chat = Chat.get_chat_by_id(chat_id)
    return jsonify({
        '_id': chat.id,
        'customer': {
            '_id': chat.customer.id,
            'first_name': chat.customer.first_name,
            'full_name': chat.customer.full_name,
        },
        'messages': [
            {
                '_id': message.id,
                'text': message.text,
                'timestamp': message.timestamp,
            } for message in chat.messages
        ],
    }), 200


class Message(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    chat_id = db.Column(
        db.Integer(), db.ForeignKey('chat.id'), nullable=False)
    sender = db.Column(
        db.Enum('customer', 'employee', name='sender_enum'), nullable=False)
    text = db.Column(db.String(), nullable=False)
    timestamp = db.Column(db.BigInteger(), nullable=False)


class Chat(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    customer_id = db.Column(
        db.Integer(), db.ForeignKey('customer.id'), nullable=False)
    employee_id = db.Column(
        db.Integer(), db.ForeignKey('employee.id'))
    last_timestamp = db.Column(db.BigInteger(), nullable=False)
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


class Employee(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String(), unique=True)
    password = db.Column(db.String())
    chats = db.relationship(
        'Chat', backref='employee', lazy='selectin',
        order_by=Chat.last_timestamp)

    def __init__(self, email, password):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
