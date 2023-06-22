from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from reservation.models import Schedule
from reservation.forms import ScheduleForm
import pytest

current_datetime = timezone.now()


@pytest.fixture
def create_and_save_schedule(create_schedule):
    create_schedule.professional_id.save()
    create_schedule.save()
    return create_schedule


@pytest.mark.django_db
class TestSchedule:
    def test_create_schedule(self, create_professional, client):
        professional = create_professional(

        )
        client.force_login(professional.user)
        response = client.get(reverse('schedule_new'))
        assert response.status_code == 200
        assert 'reservation/schedule.html' in response.templates[0].name
        data = {
            'start_day': (current_datetime + timedelta(days=4)).replace(hour=10, minute=0,
                                                                        second=0, microsecond=0),
            'end_day': (current_datetime + timedelta(days=4)).replace(hour=18, minute=0,
                                                                      second=0, microsecond=0),
            'meeting_time': 60
        }

        form = ScheduleForm(data)
        assert form.is_valid()

        response = client.post(reverse('schedule_new'), data)
        assert response.status_code == 302
        assert Schedule.objects.filter(professional_id=professional).count() == 2
        assert response.url == reverse('calendar')

    def test_create_schedule_invalid_data(self, create_professional, client):
        professional = create_professional(

        )
        client.force_login(professional.user)
        data = {
            'start_day': (current_datetime + timedelta(days=4)).replace(hour=10, minute=0,
                                                                        second=0, microsecond=0),
            'end_day': (current_datetime + timedelta(days=4)).replace(hour=9, minute=0,
                                                                      second=0, microsecond=0),
            'meeting_time': 60
        }
        response = client.post(reverse('schedule_new'), data)
        assert response.status_code == 302
        assert Schedule.objects.filter(professional_id=professional).count() == 1
        assert response.url == reverse('schedule_new')

    def test_create_schedule_already_exists(self, create_professional, client):
        professional = create_professional(

        )
        client.force_login(professional.user)
        data = {
            'start_day': (current_datetime + timedelta(days=5)).replace(hour=10, minute=0,
                                                                        second=0, microsecond=0),
            'end_day': (current_datetime + timedelta(days=5)).replace(hour=18, minute=0,
                                                                      second=0, microsecond=0),
            'meeting_time': 60
        }
        response = client.post(reverse('schedule_new'), data)
        assert response.status_code == 302
        assert response.url == reverse('schedule_new')
        assert Schedule.objects.filter(professional_id=professional).count() == 1

    def test_schedule_details(self, create_professional, client, create_and_save_schedule):
        professional = create_professional(

        )
        client.force_login(professional.user)
        url = reverse('schedule_detail', args=[create_and_save_schedule.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert 'reservation/schedule_details.html' in response.templates[0].name

    def test_schedule_edit(self, create_professional, client, create_and_save_schedule):
        professional = create_professional(

        )
        client.force_login(professional.user)
        start_day = (current_datetime + timedelta(days=5)).replace(hour=10, minute=0,
                                                                   second=0, microsecond=0)
        end_day = (current_datetime + timedelta(days=5)).replace(hour=16, minute=0,
                                                                 second=0, microsecond=0)
        url = reverse('schedule_edit', args=[create_and_save_schedule.pk])
        response = client.get(url)
        assert response.status_code == 200
        data = {
            'start_day': start_day,
            'end_day': end_day,
            'meeting_time': 60
        }
        form = ScheduleForm(data)
        assert form.is_valid()

        response = client.post(url, data)
        assert response.status_code == 302
        create_and_save_schedule.refresh_from_db()
        assert create_and_save_schedule.start_day == start_day
        assert create_and_save_schedule.end_day == end_day
        assert Schedule.objects.filter(professional_id=professional).count() == 1
        assert response.url == reverse('schedule_detail', args=[create_and_save_schedule.pk])

    def test_schedule_delete(self, create_professional, client, create_and_save_schedule):
        professional = create_professional(

        )
        client.force_login(professional.user)
        url = reverse('remove_schedule', args=[create_and_save_schedule.pk])
        response = client.get(url)
        assert response.status_code == 200
        assert 'reservation/schedule_delete.html' in response.template_name
        response = client.post(url)
        assert response.status_code == 302
        assert response.url == reverse('calendar')
        assert not Schedule.objects.filter(pk=create_and_save_schedule.pk).exists()
        assert Schedule.objects.filter(professional_id=professional).count() == 0
