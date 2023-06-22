import pytest
from django.urls import reverse
from reservation.models import Appointment


@pytest.mark.django_db
class TestAppointmentList:
    def test_appointment_list_as_professional(self, create_professional, client, create_appointment):
        professional = create_professional(

        )
        appointment = create_appointment()
        client.force_login(professional.user)
        response = client.get(reverse('my_appointments'))
        assert response.status_code == 200
        assert 'reservation/my_appointments_list.html' in response.templates[0].name
        assert response.context['is_professional'] is True
        my_appointments = response.context['my_appointments']
        assert len(my_appointments) == 1
        assert my_appointments[0] == appointment

    def test_appointment_list_as_client(self, create_user, client, create_appointment):
        user = create_user(

        )
        appointment = create_appointment(user=user)
        client.force_login(user)
        response = client.get(reverse('my_appointments'))
        assert response.status_code == 200
        assert 'reservation/my_appointments_list.html' in response.templates[0].name
        assert response.context['is_professional'] is False
        my_appointments = response.context['my_appointments']
        assert len(my_appointments) == 1
        assert my_appointments[0] == appointment


@pytest.mark.django_db
class TestAppointmentDelete:
    def test_appointment_delete_by_professional(self, create_professional, client, create_appointment):
        professional = create_professional(

        )
        appointment = create_appointment()
        client.force_login(professional.user)
        response = client.post(reverse('appointment_delete', kwargs={'pk': appointment.pk}))
        assert response.status_code == 302
        assert response.url == reverse('my_appointments')
        assert Appointment.objects.filter(professional_id=professional).count() == 0

    def test_appointment_delete_by_client(self, create_user, client, create_appointment):
        user = create_user(

        )
        appointment = create_appointment(user=user)
        client.force_login(user)
        response = client.post(reverse('appointment_delete', kwargs={'pk': appointment.pk}))
        assert response.status_code == 302
        assert response.url == reverse('my_appointments')
        assert Appointment.objects.filter(client_id=client1).count() == 0
