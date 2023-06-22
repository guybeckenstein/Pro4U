from chat.models import Message
from django.urls import reverse
import pytest


@pytest.mark.django_db
def test_get_chat(client, create_professional, create_user):
    user = create_user()
    client.force_login(user)
    professional = create_professional()
    url = reverse('chat_message', args=[professional.user])
    response = client.get(url)
    assert response.status_code == 200
    assert 'chat/message.html' in response.templates[0].name


@pytest.mark.django_db
def test_send_message_from_professional_to_client(client, create_professional, create_user):
    user = create_user()
    professional = create_professional()
    client.force_login(professional.user)

    post_data = {
        'msg_sent': 'Test message!',
    }

    url = reverse('chat_message', args=[user])
    response = client.post(url, post_data)

    assert response.status_code == 200

    last_message_in_chat = Message.filter_chat_by_professional_and_user(
        professional=professional, user=user
    ).latest('date')

    assert last_message_in_chat.message == 'Test message!'


@pytest.mark.django_db
def test_send_message_from_client_to_professional(client, create_professional, create_user):
    user = create_user()
    client.force_login(user)
    professional = create_professional()

    post_data = {
        'msg_sent': 'Test message!',
    }

    url = reverse('chat_message', args=[professional.user])
    response = client.post(url, post_data)

    assert response.status_code == 200

    last_message_in_chat = Message.filter_chat_by_professional_and_user(
        professional=professional, user=user
    ).latest('date')

    assert last_message_in_chat.message == 'Test message!'


@pytest.mark.django_db
def test_cant_send_empty_message(client, create_professional, create_user):
    user = create_user()
    client.force_login(user)

    url = reverse('chat_message', args=[user])

    post_data = {
        'msg_sent': 'The message sent before the empty message',
    }

    response = client.post(url, post_data)
    assert response.status_code == 200

    post_data = {
        'msg_sent': '',
    }

    response = client.post(url, post_data)
    assert response.status_code == 200

    # Retrieve the last message in the chat
    professional = create_professional()
    chat_messages = Message.filter_chat_by_professional_and_user(
        professional=professional, user=user
    ).order_by('-date')

    # Verify the last message
    assert chat_messages.count() == 1
    last_message_in_chat = chat_messages[0]
    assert last_message_in_chat.message == 'The message sent before the empty message'


@pytest.mark.django_db
def test_all_chats(client, create_professional, create_user):
    url = reverse('all_chats')

    user = create_user()
    client.force_login(user)
    response = client.get(url)

    assert response.status_code == 200
    assert 'chat/message.html' in response.templates[0].name

    chat = response.context['chat']
    contacts = Message.filter_chats_by_user(user)
    assert chat == contacts

    professional = create_professional()
    client.force_login(professional.user)
    response = client.get(url)

    assert response.status_code == 200
    assert 'chat/message.html' in response.templates[0].name

    chat = response.context['chat']
    contacts = Message.filter_chats_by_professional(professional)
    assert chat == contacts
