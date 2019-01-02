# -*- coding: utf-8 -*-

from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
lm = LoginManager()


@lm.user_loader
def load_employee(employee_id):
    return Employee.get_employee_by_id(int(employee_id))


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
    intent = db.Column(db.String())
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
    facebook_id = db.Column(db.String(), nullable=False, unique=True)
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
    email = db.Column(db.String(), nullable=False, unique=True)
    first_name = db.Column(db.String(), nullable=False)
    password = db.Column(db.String())
    chats = db.relationship(
        'Chat', backref='employee', lazy='selectin',
        order_by=Chat.last_timestamp)

    def __init__(self, email, password):
        self.email = email
        self.first_name = email.split('@')[0].capitalize()
        self.password = bcrypt.generate_password_hash(password).decode('utf8')

    @staticmethod
    def get_employee_by_email_and_password(email, password):
        employee = Employee.query.filter(Employee.email == email).one_or_none()
        if employee and bcrypt.check_password_hash(employee.password, password):
            return employee

    @staticmethod
    def get_employee_by_id(employee_id):
        return Employee.query.filter(Employee.id == employee_id).one_or_none()
