# -*- coding: utf-8 -*-

import json
from unittest import mock

import attr
from flask import url_for


@attr.s
class MockEmployee:
    id = attr.ib(default=1)
    email = attr.ib(default='barbara@contoso.com')
    password = attr.ib(default='password')
    chats = attr.ib(factory=list)


@attr.s
class MockCustomer:
    id = attr.ib(default=1)
    facebook_id = attr.ib(default='4')
    first_name = attr.ib(default='Mark')
    full_name = attr.ib(default='Mark Zuckerberg')
    chats = attr.ib(factory=list)


@attr.s
class MockChat:
    id = attr.ib(default=1)
    customer = attr.ib(factory=MockCustomer)
    customer_id = attr.ib(default=1)
    employee = attr.ib(factory=MockEmployee)
    employee_id = attr.ib(default=1)
    last_timestamp = attr.ib(default=1545592338658)
    entities = attr.ib(factory=list)
    messages = attr.ib(factory=list)


@attr.s
class MockEntity:
    id = attr.ib(default=1)
    chat = attr.ib(factory=MockChat)
    chat_id = attr.ib(default=1)
    snippet = attr.ib(default='Paris')
    type = attr.ib(default='LOC')


@attr.s
class MockMessage:
    id = attr.ib(default=1)
    chat = attr.ib(factory=MockChat)
    chat_id = attr.ib(default=1)
    sender = attr.ib(default='customer')
    text = attr.ib(default='Cool app!')
    timestamp = attr.ib(default=1545592339658)


def test_root_returns_200_and_renders_a_template(client):
    response = client.get(url_for('root'))

    assert response.status_code == 200
    assert b'Contoso ACE' in response.data


def test_webhook_get_returns_200_on_successful_challenge(client, config, mocker):
    mocker.patch.dict(config, {'FACEBOOK_VERIFY_TOKEN': 'SECRET'})

    response = client.get(
        url_for('webhook_get', **{
            'hub.challenge': 'CHALLENGE',
            'hub.mode': 'subscribe',
            'hub.verify_token': 'SECRET',
        })
    )

    assert response.status_code == 200
    assert b'CHALLENGE' in response.data


def test_wehook_get_returns_403_on_failed_challenge(client, config, mocker):
    mocker.patch.dict(config, {'FACEBOOK_VERIFY_TOKEN': 'SECRET'})

    response = client.get(
        url_for('webhook_get', **{
            'hub.challenge': 'CHALLENGE',
            'hub.mode': 'subscribe',
            'hub.verify_token': 'WRONG',
        })
    )

    assert response.status_code == 403
    assert b'FACEBOOK_VERIFY_TOKEN' in response.data


def test_webhook_post_returns_200_and_handles_the_event(client, config, mocker):
    mock_session = mocker.patch('app.db.session')
    mocker.patch('app.MessengerClient.get_user_data', return_value={
        'first_name': 'Mark',
        'last_name': 'Zuckerberg',
    })
    mocker.patch.dict(config, {'FACEBOOK_PAGE_TOKEN': 'SECRET'})

    response = client.post(
        url_for('webhook_post'),
        content_type='application/json',
        data=json.dumps({
            'entry': [
                {
                    'messaging': [
                        {
                            'message': {
                                'text': 'Cool app!',
                            },
                            'sender': {
                                'id': '4',
                            },
                            'timestamp': 1545592339658,
                        },
                    ],
                },
            ],
        }),
    )

    assert mock_session.add.call_count == 3
    assert mock_session.commit.call_count == 3
    mock_session.commit.assert_has_calls([
        mock.call(), mock.call(), mock.call()])
    assert response.status_code == 200
    assert b'OK' in response.data


def test_webhook_post_modifies_the_current_chat_if_it_exists(client, config, mocker):
    mock_session = mocker.patch('app.db.session')
    mocker.patch(
        'app.Customer.get_customer_by_facebook_id',
        return_value=MockCustomer(chats=[MockChat()]))
    mocker.patch.dict(config, {'FACEBOOK_PAGE_TOKEN': 'SECRET'})

    response = client.post(
        url_for('webhook_post'),
        content_type='application/json',
        data=json.dumps({
            'entry': [
                {
                    'messaging': [
                        {
                            'message': {
                                'text': 'I hope they like it in Paris.',
                            },
                            'sender': {
                                'id': '4',
                            },
                            'timestamp': 1545592340658,
                        },
                    ],
                },
            ],
        }),
    )

    assert mock_session.add.call_count == 2
    assert mock_session.commit.call_count == 2
    mock_session.commit.assert_has_calls([mock.call(), mock.call()])
    assert response.status_code == 200
    assert b'OK' in response.data


def test_api_chats_returns_200_and_the_unassigned_chats(client, mocker):
    mocker.patch('app.Chat.get_unassigned_chats', return_value=[
        MockChat(
            messages=[
                MockMessage(),
                MockMessage(
                    id=2, text='I hope they like it in Paris.', timestamp=1545592340658),
            ],
        ),
    ])

    response = client.get(url_for('api_chats'))

    assert response.status_code == 200

    expected = [
        {
            '_id': 1,
            'customer': {
                '_id': 1,
                'full_name': 'Mark Zuckerberg',
            },
            'message': {
                '_id': 1,
                'text': 'Cool app!',
                'timestamp': 1545592339658,
            },
        },
    ]
    result = json.loads(response.data)

    assert expected == result


def test_api_chat_by_id_returns_200_and_the_requested_chat(client, mocker):
    mocker.patch('app.current_user', MockEmployee())
    mocker.patch('app.Chat.get_chat_by_id', return_value=MockChat(
        entities=[MockEntity()],
        messages=[
            MockMessage(),
            MockMessage(
                id=2, text='I hope they like it in Paris.', timestamp=1545592340658),
        ],
    ))

    response = client.get(url_for('api_chat_by_id', chat_id=1))

    assert response.status_code == 200

    expected = {
        '_id': 1,
        'customer': {
            '_id': 1,
            'first_name': 'Mark',
            'full_name': 'Mark Zuckerberg',
        },
        'entities': [
            {
                '_id': 1,
                'snippet': 'Paris',
                'type': 'LOC',
            },
        ],
        'messages': [
            {
                '_id': 1,
                'text': 'Cool app!',
                'timestamp': 1545592339658,
            },
            {
                '_id': 2,
                'text': 'I hope they like it in Paris.',
                'timestamp': 1545592340658,
            },
        ],
    }
    result = json.loads(response.data)

    assert expected == result


def test_api_chat_by_id_returns_403_when_chat_is_not_assigned_to_employee(client, mocker):
    mocker.patch('app.current_user', MockEmployee(id=2))
    mocker.patch('app.Chat.get_chat_by_id', return_value=MockChat())

    response = client.get(url_for('api_chat_by_id', chat_id=1))

    assert response.status_code == 403


def test_api_chat_add_employee_returns_200_when_chat_is_not_assigned_to_employee(client, mocker):
    mock_session = mocker.patch('app.db.session')
    mocker.patch('app.current_user', MockEmployee())
    mocker.patch('app.Chat.get_chat_by_id', return_value=MockChat(employee_id=None))

    response = client.post(url_for('api_chat_add_employee', chat_id=1))

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once_with()
    assert response.status_code == 200


def test_api_chat_add_employee_returns_403_when_chat_is_assigned_to_employee(client, mocker):
    mock_session = mocker.patch('app.db.session')
    mocker.patch('app.Chat.get_chat_by_id', return_value=MockChat())

    response = client.post(url_for('api_chat_add_employee', chat_id=1))

    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    assert response.status_code == 403


def test_api_chat_add_entity_returns_200(client, mocker):
    mock_session = mocker.patch('app.db.session')
    mocker.patch('app.current_user', MockEmployee())
    mocker.patch('app.Chat.get_chat_by_id', return_value=MockChat())

    response = client.post(
        url_for('api_chat_add_entity', chat_id=1),
        content_type='application/json',
        data=json.dumps({
            'snippet': 'Paris',
            'type': 'LOC',
        }),
    )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once_with()
    assert response.status_code == 200


def test_api_chat_add_entity_returns_403_when_chat_is_not_assigned_to_employee(client, mocker):
    mocker.patch('app.current_user', MockEmployee(id=2))
    mocker.patch('app.Chat.get_chat_by_id', return_value=MockChat())

    response = client.post(
        url_for('api_chat_add_entity', chat_id=1),
        content_type='application/json',
        data=json.dumps({
            'snippet': 'Paris',
            'type': 'LOC',
        }),
    )

    assert response.status_code == 403


def test_api_chat_add_message_returns_200(client, config, mocker):
    mock_send = mocker.patch('app.MessengerClient.send')
    mock_session = mocker.patch('app.db.session')
    mocker.patch('app.current_user', MockEmployee())
    mocker.patch('app.Chat.get_chat_by_id', return_value=MockChat())
    mocker.patch.dict(config, {'FACEBOOK_PAGE_TOKEN': 'SECRET'})

    response = client.post(
        url_for('api_chat_add_message', chat_id=1),
        content_type='application/json',
        data=json.dumps({'text': 'Thanks! I hope so too.'}),
    )

    mock_send.assert_called_once_with(
        {'text': 'Thanks! I hope so too.'},
        {'sender': {'id': '4'}},
        'RESPONSE',
    )
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once_with()
    assert response.status_code == 200


def test_api_chat_add_message_returns_403_when_chat_is_not_assigned_to_employee(client, mocker):
    mocker.patch('app.current_user', MockEmployee(id=2))
    mocker.patch('app.Chat.get_chat_by_id', return_value=MockChat())

    response = client.post(
        url_for('api_chat_add_message', chat_id=1),
        content_type='application/json',
        data=json.dumps({'text': 'Thanks! I hope so too.'}),
    )

    assert response.status_code == 403


def test_api_employees_login_returns_200_on_successful_login(client, mocker):
    mock_login_user = mocker.patch('app.login_user')
    mocker.patch('app.Employee.get_employee_by_email_and_password', return_value=MockEmployee())

    response = client.post(
        url_for('api_employees_login'),
        content_type='application/json',
        data=json.dumps({
            'email': 'barbara@contoso.com',
            'password': 'password',
        }),
    )

    mock_login_user.assert_called_once()
    assert response.status_code == 200


def test_api_employees_login_returns_403_on_failed_login(client, mocker):
    mock_login_user = mocker.patch('app.login_user')
    mocker.patch('app.Employee.get_employee_by_email_and_password', return_value=None)

    response = client.post(
        url_for('api_employees_login'),
        content_type='application/json',
        data=json.dumps({
            'email': 'barbara@contoso.com',
            'password': 'wrong password',
        }),
    )

    mock_login_user.assert_not_called()
    assert response.status_code == 403


def test_api_employees_logout_returns_200_on_successful_logout(client, mocker):
    mock_logout_user = mocker.patch('app.logout_user')

    response = client.post(url_for('api_employees_logout'))

    mock_logout_user.assert_called_once_with()
    assert response.status_code == 200
