# -*- coding: utf-8 -*-

import os

from flask import Flask

from .models import bcrypt, db, lm
from .views import app as blueprint


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')

    FACEBOOK_PAGE_TOKEN = os.getenv('FACEBOOK_PAGE_TOKEN')
    FACEBOOK_VERIFY_TOKEN = os.getenv('FACEBOOK_VERIFY_TOKEN')

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__, template_folder='static')
app.config.from_object(Config)

bcrypt.init_app(app)
db.init_app(app)
lm.init_app(app)

app.register_blueprint(blueprint)
