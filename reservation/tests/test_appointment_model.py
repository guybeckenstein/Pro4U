from account.models import User
from account.models.professional import Professional
from conftest import USER_INFORMATION, TYPE_OF_JOB_NAME, BIRTHDAY
from reservation.models import Appointment, PriceList
from datetime import timedelta
from django.utils import timezone
import pytest

DATE = timezone.now() + timedelta(days=5)
START = DATE.replace(hour=13, minute=0, second=0, microsecond=0)
END = DATE.replace(hour=14, minute=0, second=0, microsecond=0)
SUMMARY = ""


@pytest.fixture
def create_and_save_single_appointment(create_professional, create_professional_job, create_user, create_appointment):
    professional: Professional = create_professional(
        phone_number=USER_INFORMATION.get('phone_number')[2],
        password=USER_INFORMATION.get('password')[2],
        email=USER_INFORMATION.get('email')[2],
        user_type=User.UserType.PROFESSIONAL
    )
    job: PriceList = create_professional_job(professional=professional, job_name="Gel nail polish", price=90)
    user: User = create_user(
        phone_number='987654379',
        password='testpassword9',
        email='test2@test.com',
        date_of_birth=BIRTHDAY,
        user_type=User.UserType.CLIENT,

        first_name=USER_INFORMATION.get('first_name')[0],
        last_name=USER_INFORMATION.get('last_name')[0],
        country=USER_INFORMATION.get('country')[0],
        city=USER_INFORMATION.get('city')[0],
        address=USER_INFORMATION.get('address')[0],
    )
    appointment: Appointment = create_appointment(professional=professional, user=user, job=job)
    return {'appointment': appointment, 'job': job, 'user': user, 'professional': professional}


@pytest.fixture
def create_and_save_appointments(create_appointment, create_and_save_single_appointment):
    res_dict: dict = create_and_save_single_appointment
    professional = res_dict['professional']
    user = res_dict['user']
    job = res_dict['job']

    appointment = res_dict['appointment']
    appointment2 = create_appointment(
        professional=professional,
        user=user,
        job=job,
        start=DATE.replace(hour=12, minute=0, second=0, microsecond=0),
        end=DATE.replace(hour=13, minute=0, second=0, microsecond=0),
        summary=""
    )

    return {'appointments': [appointment, appointment2], 'professional': professional, 'user': user}


@pytest.mark.django_db()
class TestAppointmentModel:
    def test_create_appointment(self, create_and_save_single_appointment):
        res_dict: dict = create_and_save_single_appointment
        appointment = res_dict['appointment']
        assert appointment.professional == res_dict['professional']
        assert appointment.user == res_dict['user']
        assert appointment.start == START
        assert appointment.end == END
        assert appointment.summary == SUMMARY
        assert appointment.job == res_dict['job']
        assert appointment in Appointment.objects.all()

    def test_delete_appointment_job(self, create_and_save_single_appointment):
        res_dict: dict = create_and_save_single_appointment
        appointment = res_dict['appointment']
        appointment.job.delete()
        assert appointment.job not in PriceList.objects.all()

    def test_delete_appointment_professional(self, create_and_save_single_appointment):
        res_dict: dict = create_and_save_single_appointment
        appointment = res_dict['appointment']
        appointment.professional.delete()
        assert appointment.professional not in Professional.objects.all()

    def test_delete_appointment_user(self, create_and_save_single_appointment):
        res_dict: dict = create_and_save_single_appointment
        appointment = res_dict['appointment']
        appointment.user.delete()
        assert appointment.user not in User.objects.all()

    def test_delete_appointment(self, create_and_save_single_appointment):
        res_dict: dict = create_and_save_single_appointment
        appointment = res_dict['appointment']
        appointment.delete()
        assert appointment not in Appointment.objects.all()

    def test_filter_appointments_from_now_by_professional(self, create_and_save_appointments):
        appointments: list = create_and_save_appointments['appointments']
        professional: Professional = create_and_save_appointments['professional']
        assert appointments == Appointment.filter_appointments_from_now(user=professional, user_type=True)

    def test_filter_appointments_from_now_by_client(self, create_and_save_appointments):
        appointments: list = create_and_save_appointments['appointments']
        user: User = create_and_save_appointments['user']
        assert appointments == Appointment.filter_appointments_from_now(user=user, user_type=False)
