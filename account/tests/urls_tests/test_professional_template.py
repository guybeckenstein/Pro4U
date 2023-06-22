import pytest
from account.tests.urls_tests.test_general import PROFILE_URL


@pytest.mark.django_db
class TestProfessionalProfile:
    def test_get_professional_profile(self, create_professional, client):
        professional = create_professional(

        )
        client.force_login(professional.user)
        response = client.get(f"{PROFILE_URL}")
        assert response.status_code == 200
        assert 'account/profile.html' in [template.name for template in response.templates]
        assert f"{professional.user.first_name}'s Profile" in response.content.decode('utf-8')
        assert 'Type Of Jobs' in response.content.decode('utf-8')
        assert 'Schedule' in response.content.decode('utf-8')
        assert 'media/default.png' in response.content.decode('utf-8')

    def test_profile_template_inheritance(self, create_professional, client):
        urls = ['settings/']
        professional = create_professional(

        )
        client.force_login(professional.user)

        for url in urls:
            response = client.get(f"{PROFILE_URL}{url}")
            assert 'account/profile.html' in [template.name for template in response.templates]

    def test_get_professional_profile_settings(self, create_professional, client):
        professional = create_professional(

        )
        client.force_login(professional.user)
        response = client.get(f"{PROFILE_URL}settings/")
        assert response.status_code == 200
        assert 'account/profile_settings.html' in [template.name for template in response.templates]
        assert professional.user.username in response.content.decode()
        assert professional.user.first_name in response.content.decode()
        assert professional.user.last_name in response.content.decode()
        assert professional.user.email in response.content.decode()
        assert professional.user.phone_number in response.content.decode()
        assert professional.user.country in response.content.decode()
        assert professional.user.city in response.content.decode()
        assert professional.user.address in response.content.decode()
        assert professional.profession in response.content.decode()
