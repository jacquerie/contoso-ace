# -*- coding: utf-8 -*-

import os

from flask import Flask

from .cli import db_cli, employee_cli
from .models import bcrypt, db, lm
from .views import app as blueprint


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    FACEBOOK_PAGE_TOKEN = os.getenv('FACEBOOK_PAGE_TOKEN')
    FACEBOOK_VERIFY_TOKEN = os.getenv('FACEBOOK_VERIFY_TOKEN')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(
    __name__,
    template_folder=os.path.join('client', 'build'),
    static_folder=os.path.join('client', 'build', 'static'),
)
app.config.from_object(Config)

app.cli.add_command(db_cli)
app.cli.add_command(employee_cli)

bcrypt.init_app(app)
db.init_app(app)
lm.init_app(app)

app.register_blueprint(blueprint)
