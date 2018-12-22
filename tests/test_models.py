# -*- coding: utf-8 -*-

from app import Employee


def test_employee_encrypts_passwords_on_creation():
    employee = Employee('employee@example.com', 'password')
    assert employee.password != 'password'
