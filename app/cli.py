# -*- coding: utf-8 -*-

from flask.cli import AppGroup, with_appcontext

from .models import db

db_cli = AppGroup('db')


@db_cli.command('create')
@with_appcontext
def db_create():
    db.create_all()


@db_cli.command('drop')
@with_appcontext
def db_drop():
    db.drop_all()
