# -*- coding: utf-8 -*-

from pytest import fixture

from app import app as _app


@fixture
def app():
    yield _app
