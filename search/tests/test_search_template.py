from account.models.professional import Professional
from reservation.models import PriceList
from django.urls import reverse
import pytest

CLIENT_ID = 2


@pytest.mark.django_db
class TestSearchTemplate:
    def test_search_page(self, client):
        url = reverse('search-history', args=[CLIENT_ID])
        response = client.get(url)
        assert response.status_code == 200
        assert 'search/search.html' in response.templates[0].name

    def test_search_by_no_filters(self, client):
        url = reverse('search-history', args=[CLIENT_ID])
        response = client.post(url, {})
        professionals = response.context['professionals']
        assert list(professionals) == list(Professional.objects.all())

    def test_search_by_professional_id(self, client, create_professional):
        professional = create_professional()
        url = reverse('search-history', args=[CLIENT_ID])
        data = {
                'professional_id': professional.id
            }
        response = client.post(url, data)

        assert response.status_code == 200
        assert 'search/search.html' in response.templates[0].name

        professionals = response.context['professionals']
        assert len(professionals) == len(Professional.objects.all())
        assert professionals.last().id == professional.id
        assert professionals.last().profession == professional.profession
        assert professionals.last().user.first_name == professional.user.first_name
        assert professionals.last().user.last_name == professional.user.last_name
        assert professionals.last().user.city == professional.user.city


    def test_redirection_to_professional_page(self, client, create_professional):
        professional_user = create_professional()
        type_of_jobs = PriceList.get_type_of_jobs_by_professional(professional_id=professional_user.professional_id)
        client.force_login(professional_user.user)
        url = reverse('show-professional', kwargs={'professional_id': professional_user.professional_id})
        data = {
            'professional': professional_user, 'type_of_jobs': type_of_jobs
        }

        response = client.post(url, data)

        assert response.status_code == 200
        assert 'account/business_page.html' in [template.name for template in response.templates]
        assert f"{professional_user.get_profession_display()}" in response.content.decode('utf-8')
        assert f"{professional_user.user.first_name}" in response.content.decode('utf-8')
        assert f"{professional_user.user.last_name}" in response.content.decode('utf-8')
