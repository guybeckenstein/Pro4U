import pytest
from account.tests.urls_tests.test_general import PROFILE_URL
from django.urls import reverse
from conftest import USER_INFORMATION


@pytest.fixture
def user(create_user):
    user = create_user(

    )
    user.save()
    return user


@pytest.mark.django_db
class TestClientProfile:
    def test_get_client_profile(self, create_user, client):
        user = create_user(

        )
        client.force_login(user)
        response = client.get(f"{PROFILE_URL}")
        assert response.status_code == 200
        assert 'account/profile.html' in [template.name for template in response.templates]
        assert f"{user.first_name}'s Profile" in response.content.decode('utf-8')
        assert 'Search' in response.content.decode('utf-8')
        assert 'media/default.png' in response.content.decode('utf-8')

    def test_profile_template_inheritance(self, create_user, client):
        urls = ['settings/']
        user = create_user(

        )
        client.force_login(user)

        for url in urls:
            response = client.get(f"{PROFILE_URL}{url}")
            assert 'account/profile.html' in [template.name for template in response.templates]

    def test_get_client_profile_settings(self, create_user, client):
        user = create_user(

        )
        client.force_login(user)
        response = client.get(f"{PROFILE_URL}settings/")
        assert response.status_code == 200
        assert 'account/profile_settings.html' in [template.name for template in response.templates]
        assert user.username in response.content.decode()
        assert user.first_name in response.content.decode()
        assert user.last_name in response.content.decode()
        assert user.email in response.content.decode()
        assert user.phone_number in response.content.decode()
        assert user.country in response.content.decode()
        assert user.city in response.content.decode()
        assert user.address in response.content.decode()
        assert 'Jan. 1, 2000' in response.content.decode()

    def test_get_client_profile_edit(self, create_user, client):
        user = create_user(

        )
        client.force_login(user)
        response = client.get(f"{PROFILE_URL}edit/")
        assert response.status_code == 200
        assert 'account/update_profile.html' in [template.name for template in response.templates]

        data = {
            'username': USER_INFORMATION.get('username')[1],
            'first_name': USER_INFORMATION.get('first_name')[1],
            'last_name': USER_INFORMATION.get('last_name')[1],
            'email': USER_INFORMATION.get('email')[1],
            'phone_number': USER_INFORMATION.get('phone_number')[1],
            'country': USER_INFORMATION.get('country')[1],
            'city': USER_INFORMATION.get('city')[1],
            'address': USER_INFORMATION.get('address')[1]
        }
        response = client.post(f"{PROFILE_URL}edit/", data)
        assert response.status_code == 302
        user.refresh_from_db()
        assert user.username == USER_INFORMATION.get('username')[1]
        assert user.first_name == USER_INFORMATION.get('first_name')[1]
        assert user.last_name == USER_INFORMATION.get('last_name')[1]
        assert user.email == USER_INFORMATION.get('email')[1]
        assert user.phone_number == USER_INFORMATION.get('phone_number')[1]
        assert user.country == USER_INFORMATION.get('country')[1]
        assert user.city == USER_INFORMATION.get('city')[1]
        assert user.address == USER_INFORMATION.get('address')[1]
        assert response.url == reverse('profile_settings')

    def test_get_professional_business_page(self, create_user, client, create_professional):
        user = create_user(

        )
        client.force_login(user)
        professional = create_professional(username=USER_INFORMATION.get('username')[1],
                                                password=USER_INFORMATION.get('password')[1],
                                                email=USER_INFORMATION.get('email')[1],
                                                phone_number=USER_INFORMATION.get('phone_number')[1])
        response = client.get(f"{PROFILE_URL}professional/{professional.id}/")
        assert response.status_code == 200
        assert 'account/business_page.html' in [template.name for template in response.templates]
        returned_professional = response.context.get("professional")
        assert returned_professional == professional
        assert f"{professional.get_profession_display()}" in response.content.decode('utf-8')
        assert f"{professional.user.first_name}" in response.content.decode('utf-8')
        assert f"{professional.user.last_name}" in response.content.decode('utf-8')
