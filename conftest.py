# -*- coding: utf-8 -*-

from pytest import fixture

from app import app as _app


@fixture
def app():
    _app.config['LOGIN_DISABLED'] = True
    _app.login_manager.init_app(_app)
    yield _app
