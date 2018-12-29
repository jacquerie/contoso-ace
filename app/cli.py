# -*- coding: utf-8 -*-

import click
from flask.cli import AppGroup, with_appcontext

from .models import Employee, db

db_cli = AppGroup('db')
employee_cli = AppGroup('employee')


@db_cli.command('create')
@with_appcontext
def db_create():
    db.create_all()


@db_cli.command('drop')
@with_appcontext
def db_drop():
    db.drop_all()


@employee_cli.command('create')
@with_appcontext
@click.argument('email')
@click.argument('password')
def employee_create(email, password):
    employee = Employee(email, password)
    db.session.add(employee)
    db.session.commit()
