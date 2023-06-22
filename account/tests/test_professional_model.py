from account.models.user import User
from account.models.professional import Professional
from conftest import PROFESSIONAL_INFORMATION
import pytest


@pytest.mark.django_db
class TestProfessionalModel:
    def test_new_professional(self, create_professional):
        professional = create_professional()
        assert professional.profession == PROFESSIONAL_INFORMATION.get('profession')[0]

    def test_get_professional(self, create_professional):
        professional = create_professional()
        assert professional in Professional.objects.all()

    def test_delete_professional_only(self, create_professional):
        professional = create_professional()
        professional.delete()
        assert professional not in Professional.objects.all()

    def test_delete_professional_and_user_normal(self, create_professional):
        professional = create_professional()
        professional.user.delete()
        assert professional not in Professional.objects.all()

    def test_delete_professional_and_user_using_filter(self, create_professional):
        professional = create_professional()
        ID = professional.id
        User.objects.filter(id=Professional.objects.filter(id=ID).values_list('user', flat=True)[0]).delete()
        Professional.objects.filter(id=ID).delete()
        assert professional.user not in User.objects.all()

    def test_filter_by_profession(self, create_professional):
        professional = create_professional(
            phone_number='111111',
            password='password1',
            email='john.doe@example.com',
            user_type=User.UserType.PROFESSIONAL
        )
        professional2 = create_professional(
            phone_number='222222',
            password='password2',
            email='john2.doe@example.com',
            user_type=User.UserType.PROFESSIONAL
        )
        create_professional(
            phone_number='333333',
            password='password3',
            first_name="Tal",
            email='john3.doe@example.com',
            user_type=User.UserType.PROFESSIONAL,
            profession=Professional.Professions.Plumber
        )

        filter_query = Professional.objects.filter(profession=PROFESSIONAL_INFORMATION.get('profession')[0])
        assert list(filter_query) == [professional, professional2]
