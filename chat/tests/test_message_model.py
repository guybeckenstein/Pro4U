from account.models import User
from chat.models import Message
import pytest

from conftest import USER_INFORMATION, BIRTHDAY

MESSAGE = "message1"


@pytest.fixture
def get_saved_chat_message(create_professional, create_user, create_chat_message):
    professional = create_professional(
        phone_number=USER_INFORMATION.get('phone_number')[2],
        password=USER_INFORMATION.get('password')[2],
        email=USER_INFORMATION.get('email')[2],

        user_type=User.UserType.PROFESSIONAL
    )
    user = create_user(
        phone_number=USER_INFORMATION.get('phone_number')[0],
        password=USER_INFORMATION.get('password')[0],
        email=USER_INFORMATION.get('email')[0],
        date_of_birth=BIRTHDAY,

        first_name=USER_INFORMATION.get('first_name')[0],
        last_name=USER_INFORMATION.get('last_name')[0],
        country=USER_INFORMATION.get('country')[0],
        city=USER_INFORMATION.get('city')[0],
        address=USER_INFORMATION.get('address')[0],
        user_type=User.UserType.CLIENT
    )
    message = create_chat_message(professional=professional, user=user)
    message.save()
    return message


@pytest.mark.django_db
class TestMessageModel:
    def test_create_message(self, create_professional, create_user, create_chat_message):
        professional = create_professional(
            phone_number=USER_INFORMATION.get('phone_number')[2],
            password=USER_INFORMATION.get('password')[2],
            email=USER_INFORMATION.get('email')[2],

            user_type=User.UserType.PROFESSIONAL
        )
        user = create_user(
            phone_number=USER_INFORMATION.get('phone_number')[0],
            password=USER_INFORMATION.get('password')[0],
            email=USER_INFORMATION.get('email')[0],
            date_of_birth=BIRTHDAY,

            first_name=USER_INFORMATION.get('first_name')[0],
            last_name=USER_INFORMATION.get('last_name')[0],
            country=USER_INFORMATION.get('country')[0],
            city=USER_INFORMATION.get('city')[0],
            address=USER_INFORMATION.get('address')[0],
            user_type=User.UserType.CLIENT
        )
        message = create_chat_message(professional=professional, user=user)
        assert message.professional == professional
        assert message.user == user
        assert message.content == MESSAGE
        assert message.sender_type == Message.SenderType.CLIENT

    def test_save_message(self, get_saved_chat_message):
        assert get_saved_chat_message in Message.objects.all()

    def test_delete_message(self, get_saved_chat_message):
        message = get_saved_chat_message
        message.delete()
        assert message not in Message.objects.all()

    def test_filter_chats_by_professional(self, get_saved_chat_message):
        message = get_saved_chat_message
        assert [message.user] == Message.filter_chats_by_professional(professional=message.professional)

    def test_filter_chats_by_user(self, get_saved_chat_message):
        message = get_saved_chat_message
        assert [message.professional] == Message.filter_chats_by_user(user=message.user)

    def test_filter_chat_by_professional_and_user(self, get_saved_chat_message):
        message = get_saved_chat_message
        assert [message] == list(
            Message.filter_chat_by_professional_and_user(professional=message.professional, user=message.user)
        )
