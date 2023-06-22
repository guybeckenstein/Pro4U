import pytest
from django.urls import reverse
from reservation.models import Appointment


@pytest.fixture
def save_schedule(create_schedule):
    create_schedule.professional_id.save()
    create_schedule.save()
    return create_schedule


@pytest.mark.django_db
class TestMakeAppointment:
    def test_make_appointment_view(self, create_user, client, create_professional):
        user = create_user(

        )
        client.force_login(user)
        professional = create_professional(

        )
        response = client.get(reverse('make_appointment', kwargs={'pk': professional.pk}))
        assert response.status_code == 200
        assert 'reservation/make_appointment.html' in response.templates[0].name

    def test_confirm_appointment_view(self, create_user, client, create_professional, create_professional_job, create_and_save_schedule):
        user = create_user(

        )
        client.force_login(user)
        professional = create_professional(

        )
        new_job = create_professional_job(professional=professional)

        data = {
            'service': new_job.pk  # Include the typeOfJob selected by the user
        }

        response = client.get(reverse('confirm_appointment', kwargs={
            'professional_id': professional.pk,
            'day': create_and_save_schedule.start_day.day,
            'month': create_and_save_schedule.start_day.month,
            'year': create_and_save_schedule.start_day.year,
            'meeting': "10:00-11:00"
        }))
        assert response.status_code == 200
        assert 'reservation/confirm_appointment.html' in response.templates[0].name

        response = client.post(reverse('confirm_appointment', kwargs={
            'professional_id': professional.pk,
            'day': create_and_save_schedule.start_day.day,
            'month': create_and_save_schedule.start_day.month,
            'year': create_and_save_schedule.start_day.year,
            'meeting': '10:00-11:00'
        }), data=data)

        assert response.status_code == 302
        assert response.url == reverse('make_appointment', args=[professional.pk])
        assert Appointment.objects.filter(professional_id=professional).count() == 1
        appointment = Appointment.objects.filter(professional_id=professional).first()
        assert appointment.professional_id.professional_id == professional.pk
        assert appointment.start.year == create_and_save_schedule.start_day.year
        assert appointment.start.month == create_and_save_schedule.start_day.month
        assert appointment.start.day == create_and_save_schedule.start_day.day
        assert appointment.start.hour == 10
        assert appointment.start.minute == 0
        assert appointment.end.year == create_and_save_schedule.start_day.year
        assert appointment.end.month == create_and_save_schedule.start_day.month
        assert appointment.end.day == create_and_save_schedule.start_day.day
        assert appointment.end.hour == 11
        assert appointment.end.minute == 0
        assert appointment.user == user
