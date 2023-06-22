import pytest
from django.urls import reverse
from account.forms import LoginForm


USERNAME = "TalTheUser"
PASSWORD = 'TalPassword'


@pytest.mark.django_db
class TestLoginView:
    def test_enter_login_page(self, client):
        response = client.get('/login/')
        assert response.status_code == 200
        assert 'account/login.html' in response.templates[0].name

    def test_sign_in_POST_valid(self, client):
        response = client.post('/login/', {
            'username': USERNAME,
            'password': PASSWORD,
        })
        assert response.status_code == 302
        assert response.url == reverse('profile_landing')

    def test_sign_in_POST_invalid(self, client):
        response = client.post('/login/', {
            'username': "test2",
            'password': PASSWORD,
        })
        assert response.status_code == 200
        assert b'Invalid username or password' in response.content

    def test_login_form_validity(self):
        data = {
            'username': USERNAME,
            'password': PASSWORD,
        }

        form = LoginForm(data)
        assert form.is_valid()
