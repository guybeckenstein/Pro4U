from typing import Callable

from django.http import HttpResponse

from account.models.user import User
from account.models.professional import Professional
from chat.models import Message
from landing.models import TeamMember
from reservation.models import PriceList, Appointment, Schedule
from datetime import timedelta, datetime
from search.models import Search
from django.utils import timezone
import pytest

current_datetime = timezone.now()

BIRTHDAY = datetime(2000, 1, 1)
LAST_LOGIN = timezone.now()

TYPE_OF_JOB_NAME = "Hair cut"
PRICE = 100

USER_INFORMATION: dict[str, list] = {
    'phone_number': ['123456789', '987654321', '1212121212'],
    'password': ['testpassword', 'testpassword2', 'testpassword3'],
    'email': ['test@test.com', 'test2@test.com', 'test3@test.com'],

    'first_name': ['Bob', 'john'],
    'last_name': ['Builder', 'Doe'],
    'country': ['USA', 'Israel'],
    'city': ['New York', 'Tel Aviv'],
    'address': ['123 Main St', '456 Main St'],
}

PROFESSIONAL_INFORMATION = {
    'profession': [Professional.Professions.Locksmith, Professional.Professions.Plumber]
}


@pytest.fixture
def create_user():
    def _user_factory(phone_number, password, email, date_of_birth, user_type,
             first_name: str, last_name: str, country: str, city: str, address: str):
        user = User.objects.create_user(
            phone_number=phone_number,
            password=password,
            email=email,
            date_of_birth=date_of_birth,
            type=user_type,

            first_name=first_name,
            last_name=last_name,
            country=country,
            city=city,
            address=address,
        )
        return user

    return _user_factory


@pytest.fixture
def create_professional(create_user):
    def _professional_factory(
        phone_number: str = USER_INFORMATION.get('phone_number')[0],
        password: str = USER_INFORMATION.get('password')[0],
        email: str = USER_INFORMATION.get('email')[0],
        date_of_birth=BIRTHDAY,

        first_name: str = USER_INFORMATION.get('first_name')[0],
        last_name: str = USER_INFORMATION.get('last_name')[0],
        country: str = USER_INFORMATION.get('country')[0],
        city: str = USER_INFORMATION.get('city')[0],
        address: str = USER_INFORMATION.get('address')[0],
        user_type: User.UserType = User.UserType.PROFESSIONAL,
        profession: Professional.Professions = PROFESSIONAL_INFORMATION.get('profession')[0],
    ):
        professional = Professional.objects.create(
            user=create_user(
                phone_number=phone_number,
                password=password,
                email=email,
                date_of_birth=date_of_birth,
                user_type=user_type,

                first_name=first_name,
                last_name=last_name,
                country=country,
                city=city,
                address=address
            ),
            profession=profession
        )
        return professional

    return _professional_factory


@pytest.fixture
def create_chat_message():
    def _message_factory(professional, user):
        return Message(sender_type=Message.SenderType.CLIENT, professional=professional, user=user, content="message1")
    return _message_factory


@pytest.fixture
def create_professional_job(create_professional):
    def _job_factory(professional, job_name: str = TYPE_OF_JOB_NAME, price: int = 100):
        return PriceList.objects.create(professional=professional, job_name=job_name, price=price)
    return _job_factory


@pytest.fixture
def create_appointment(create_professional, create_user, create_professional_job):
    def _appointment_factory(
            professional: Professional, user: User, job: PriceList,
            start: datetime = (current_datetime + timedelta(days=5)).replace(hour=13, minute=0, second=0, microsecond=0),
            end: datetime = (current_datetime + timedelta(days=5)).replace(hour=14, minute=0, second=0, microsecond=0),
            summary: str = ""
    ):
        appointment = Appointment.objects.create(
            professional=professional, user=user, job=job, start=start, end=end, summary=summary
        )
        appointment.professional.save()
        appointment.user.save()
        appointment.job.save()
        appointment.save()
        return appointment

    return _appointment_factory


@pytest.fixture
def create_schedule(create_professional):
    def _schedule_factory(professional: Professional):
        return Schedule(
            professional=professional,
            start_day=(current_datetime + timedelta(days=5)).replace(hour=10, minute=0, second=0, microsecond=0),
            end_day=(current_datetime + timedelta(days=5)).replace(hour=18, minute=0, second=0, microsecond=0),
            meeting_time=60
        )
    return _schedule_factory


@pytest.fixture
def create_search_instance():
    def _search_instance_factory(user, professional):
        return Search(user=user, professional=professional)
    return _search_instance_factory


@pytest.fixture(scope='function')
def create_team_member() -> Callable[[str], TeamMember]:
    def _team_member_factory(name: str) -> TeamMember:
        name_without_whitespaces = ''.join(name.split())
        team_member = TeamMember(
            name=name,
            img=f'/img/{name_without_whitespaces}.jpg',
            alt=name_without_whitespaces,
        )
        return team_member
    return _team_member_factory


@pytest.fixture
def get_url() -> Callable[[str], str]:
    def _get_url_factory(view_name: str) -> str:
        from django.urls import reverse
        return reverse(view_name)

    return _get_url_factory


@pytest.fixture
def get_response(client, get_url) -> Callable[[str], HttpResponse]:
    def _get_response_factory(view_name: str) -> HttpResponse:
        url = get_url(view_name)
        return client.get(url)

    return _get_response_factory
