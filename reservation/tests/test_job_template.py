from django.urls import reverse
from reservation.models import PriceList
from reservation.forms import PriceListForm
import pytest


@pytest.fixture
def save_job(create_professional_job):
    new_job = create_professional_job()
    new_job.professional_id.save()
    new_job.save()
    return new_job


@pytest.mark.django_db
class TestTypeOfJob:
    def test_get_job_list(self, create_professional, client, create_professional_job):
        professional = create_professional(

        )
        new_job = create_professional_job(professional=professional)
        client.force_login(professional.user)
        response = client.get(reverse('jobs'))
        assert response.status_code == 200
        assert 'reservation/typeOfJob_list.html' in response.templates[0].name
        assert any(new_job.pk == existed_typeOfJob.pk for existed_typeOfJob in response.context['type_of_jobs'])

    def test_create_new_job(self, create_professional, client, save_job):
        professional = create_professional(

        )
        client.force_login(professional.user)
        response = client.get(reverse('typeOfJob_create'))
        assert response.status_code == 200
        assert 'reservation/typeOfJob_form.html' in response.templates[0].name

        data = {
            'job_name': 'Woman haircut',
            'price': 200,
        }

        response = client.post(reverse('typeOfJob_create'), data)
        assert response.status_code == 302
        assert PriceList.objects.filter(professional_id=professional).count() == 2
        assert response.url == reverse('jobs')

    def test_update_job(self, create_professional, client, save_job):
        professional = create_professional(

        )
        client.force_login(professional.user)
        url = reverse('typeOfJob_update', args=[save_job.pk])
        response = client.get(url)
        assert response.status_code == 200

        data = {
            'job_name': 'Updated Type of Job',
            'price': 150,
        }

        response = client.post(url, data)
        assert response.status_code == 302
        save_job.refresh_from_db()
        assert save_job.job_name == 'Updated Type of Job'
        assert save_job.price == 150
        assert PriceList.objects.filter(professional_id=professional).count() == 1
        assert response.url == reverse('jobs')

    def test_delete_job(self, create_professional, client, save_job):
        professional = create_professional(

        )
        client.force_login(professional.user)
        url = reverse('typeOfJob_delete', args=[save_job.pk])
        response = client.post(url)
        assert response.status_code == 302
        assert PriceList.objects.filter(professional_id=professional).count() == 0

    def test_form_validity(self):
        data = {
            'job_name': 'Woman haircut',
            'price': 200,
        }

        form = PriceListForm(data)
        assert form.is_valid()
