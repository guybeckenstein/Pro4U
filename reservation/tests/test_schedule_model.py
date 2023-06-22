from account.models import User
from account.models.professional import Professional
from conftest import USER_INFORMATION, BIRTHDAY
from reservation.models import Schedule
from datetime import timedelta
from django.utils import timezone
import pytest

DATE = timezone.now() + timedelta(days=5)
START_DAY = DATE.replace(hour=10, minute=0, second=0, microsecond=0)
END_DAY = DATE.replace(hour=18, minute=0, second=0, microsecond=0)
MEETING_TIME = 60


@pytest.fixture
def create_and_save_schedule(create_schedule, create_professional):
    professional: Professional = create_professional(
        phone_number=USER_INFORMATION.get('phone_number')[2],
        password=USER_INFORMATION.get('password')[2],
        email=USER_INFORMATION.get('email')[2],
        user_type=User.UserType.PROFESSIONAL
    )
    schedule = create_schedule(professional=professional)
    schedule.professional.save()
    schedule.save()
    return schedule


@pytest.fixture
def create_and_save_meetings(create_user, create_and_save_schedule, create_professional_job, create_appointment):
    user: User = create_user(
        phone_number='972541234',
        password='123456',
        email='john1@doe.com',
        date_of_birth=BIRTHDAY,
        user_type=User.UserType.CLIENT,

        first_name='John',
        last_name='Doe',
        country='United Kingdom',
        city='London',
        address='Address'
    )
    schedule: Schedule = create_and_save_schedule
    job = create_professional_job(professional=schedule.professional)
    appointment = create_appointment(
        professional=schedule.professional,
        user=user,
        job=job,
        start=DATE.replace(hour=12, minute=0, second=0, microsecond=0),
        end=DATE.replace(hour=13, minute=0, second=0, microsecond=0),
        summary=""
    )
    appointment2 = create_appointment(
        professional=schedule.professional,
        user=user,
        job=job,
        summary=""
    )
    save_appointment(appointment)
    save_appointment(appointment2)
    return {
        'meetings':
            [
                ["10:00-11:00", "11:00-12:00", "14:00-15:00", "15:00-16:00", "16:00-17:00", "17:00-18:00"],
                ["10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00", "15:00-16:00",
                 "16:00-17:00", "17:00-18:00"]
            ],
        'professional': schedule.professional
    }


def save_appointment(appointment):
    appointment.professional.save()
    appointment.user.save()
    appointment.job.save()
    appointment.save()


@pytest.mark.django_db()
class TestScheduleModel:
    def test_create_schedule(self, create_schedule, create_professional):
        professional: Professional = create_professional(
            phone_number=USER_INFORMATION.get('phone_number')[2],
            password=USER_INFORMATION.get('password')[2],
            email=USER_INFORMATION.get('email')[2],
            user_type=User.UserType.PROFESSIONAL
        )
        schedule: Schedule = create_schedule(professional=professional)
        assert schedule.professional == professional
        assert schedule.start_day == START_DAY
        assert schedule.end_day == END_DAY
        assert schedule.meeting_time == MEETING_TIME

    def test_save_schedule(self, create_and_save_schedule):
        schedule = create_and_save_schedule
        assert schedule in Schedule.objects.all()

    def test_delete_schedule(self, create_and_save_schedule):
        schedule = create_and_save_schedule
        schedule.delete()
        assert schedule not in Schedule.objects.all()

    def test_delete_professional(self, create_and_save_schedule):
        schedule = create_and_save_schedule
        schedule.professional.delete()
        assert schedule not in Schedule.objects.all()

    def test_get_professional_possible_meetings(self, create_and_save_meetings):
        res_dict: dict = create_and_save_meetings
        expected_meetings = res_dict['meetings'][1]
        actual_meetings = Schedule.get_professional_possible_meetings(
            professional=res_dict['professional'], day=START_DAY.day, month=START_DAY.month, year=START_DAY.year
        )
        assert expected_meetings == list(actual_meetings)

    def test_get_free_meetings_by_professional_and_date(self, create_and_save_meetings):
        res_dict: dict = create_and_save_meetings
        expected_meetings = res_dict['meetings'][0]
        actual_meetings = Schedule.get_free_meetings(
            professional=res_dict['professional'], day=START_DAY.day, month=START_DAY.month, year=START_DAY.year
        )
        assert expected_meetings == list(actual_meetings)
