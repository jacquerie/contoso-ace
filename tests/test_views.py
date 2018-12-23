# -*- coding: utf-8 -*-

import json

import attr
from flask import url_for


@attr.s
class MockChat:
    id = attr.ib()
    customer = attr.ib()
    entities = attr.ib()
    messages = attr.ib()


@attr.s
class MockCustomer:
    id = attr.ib()
    first_name = attr.ib()
    full_name = attr.ib()


@attr.s
class MockEntity:
    id = attr.ib()
    snippet = attr.ib()
    type = attr.ib()


@attr.s
class MockMessage:
    id = attr.ib()
    text = attr.ib()
    timestamp = attr.ib()


def test_root_returns_200_and_renders_a_template(client):
    response = client.get(url_for('root'))

    assert response.status_code == 200
    assert b'Contoso ACE' in response.data


def test_webhook_get_returns_200_on_successful_challenge(client, config, mocker):
    mocker.patch.dict(config, {'FACEBOOK_VERIFY_TOKEN': 'SECRET'})

    response = client.get(
        url_for('webhook_get', **{
            'hub.challenge': 'CHALLENGE',
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
            'hub.verify_token': 'WRONG',
        })
    )

    assert response.status_code == 403
    assert b'FACEBOOK_VERIFY_TOKEN' in response.data


def test_webhook_post_returns_200_and_handles_the_message(client, config, mocker):
    mocked_handler = mocker.patch('app.Messenger.handle')
    mocker.patch.dict(config, {'FACEBOOK_PAGE_TOKEN': 'SECRET'})

    webhook_event = {
        'entry': [
            {
                'messaging': [
                    {
                        'message': {
                            'text': 'Hello, world!',
                        },
                    },
                ],
            },
        ],
    }

    response = client.post(
        url_for('webhook_post'),
        content_type='application/json',
        data=json.dumps(webhook_event),
    )

    mocked_handler.assert_called_once_with(webhook_event)
    assert response.status_code == 200
    assert b'OK' in response.data


def test_api_chats_returns_200_and_the_unassigned_chats(client, mocker):
    mocker.patch('app.Chat.get_unassigned_chats', return_value=[
        MockChat(
            id=1,
            customer=MockCustomer(
                id=1, first_name='Mark', full_name='Mark Zuckerberg'),
            entities=[MockEntity(id=1, snippet='Paris', type='LOC')],
            messages=[
                MockMessage(id=1, text='Cool app!', timestamp=1545592339658),
                MockMessage(id=2, text='Good luck for Paris.', timestamp=1545592340658),
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
    mocker.patch('app.Chat.get_chat_by_id', return_value=MockChat(
        id=1,
        customer=MockCustomer(
            id=1, first_name='Mark', full_name='Mark Zuckerberg'),
        entities=[MockEntity(id=1, snippet='Paris', type='LOC')],
        messages=[
            MockMessage(id=1, text='Cool app!', timestamp=1545592339658),
            MockMessage(id=2, text='Good luck for Paris.', timestamp=1545592340658),
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
                'text': 'Good luck for Paris.',
                'timestamp': 1545592340658,
            },
        ],
    }
    result = json.loads(response.data)

    assert expected == result


def test_api_chat_add_entity_returns_200(client, mocker):
    mock_session = mocker.patch('app.db.session')

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
