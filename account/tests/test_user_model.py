from django.db.models import Q

from account.models.user import User
from conftest import USER_INFORMATION, BIRTHDAY
import pytest

INFO = {
    'phone_number': USER_INFORMATION.get('phone_number')[0],
    'password': USER_INFORMATION.get('password')[0],
    'email': USER_INFORMATION.get('email')[0],
    'date_of_birth': BIRTHDAY,
    'first_name': USER_INFORMATION.get('first_name')[0],
    'last_name': USER_INFORMATION.get('last_name')[0],
    'country': USER_INFORMATION.get('country')[0],
    'city': USER_INFORMATION.get('city')[0],
    'address': USER_INFORMATION.get('address')[0],
}


@pytest.mark.django_db
class TestUserModel:
    def test_add_user(self, create_user):
        user = create_user(
            phone_number=INFO['phone_number'],
            password=INFO['password'],
            email=INFO['email'],
            date_of_birth=INFO['date_of_birth'],
            first_name=INFO['first_name'],
            last_name=INFO['last_name'],
            country=INFO['country'],
            city=INFO['city'],
            address=INFO['address'],
            user_type=User.UserType.CLIENT,
        )
        assert user.date_of_birth == BIRTHDAY

    def test_get_user(self, create_user):
        user = create_user(
            phone_number=INFO['phone_number'],
            password=INFO['password'],
            email=INFO['email'],
            date_of_birth=INFO['date_of_birth'],
            first_name=INFO['first_name'],
            last_name=INFO['last_name'],
            country=INFO['country'],
            city=INFO['city'],
            address=INFO['address'],
            user_type=User.UserType.CLIENT,
        )
        assert user in User.objects.all()

    def test_delete_user(self, create_user):
        user = create_user(
            phone_number=INFO['phone_number'],
            password=INFO['password'],
            email=INFO['email'],
            date_of_birth=INFO['date_of_birth'],
            first_name=INFO['first_name'],
            last_name=INFO['last_name'],
            country=INFO['country'],
            city=INFO['city'],
            address=INFO['address'],
            user_type=User.UserType.CLIENT,
        )
        user.delete()
        assert user not in User.objects.all()

    def test_filter_by_first_name(self, create_user):
        user1 = create_user(
            phone_number='111111',
            password=INFO['password'],
            email='john.doe@example.com',
            date_of_birth=INFO['date_of_birth'],
            first_name=INFO['first_name'],
            last_name=INFO['last_name'],
            country=INFO['country'],
            city=INFO['city'],
            address=INFO['address'],
            user_type=User.UserType.CLIENT,
        )
        user2 = create_user(
            phone_number='222222',
            password=INFO['password'],
            email='john.doe2@example.com',
            date_of_birth=INFO['date_of_birth'],
            first_name=INFO['first_name'],
            last_name=INFO['last_name'],
            country=INFO['country'],
            city='Toronto',
            address=INFO['address'],
            user_type=User.UserType.CLIENT,
        )
        create_user(
            phone_number='333333',
            password=INFO['password'],
            email='john.doe2@example.com',
            date_of_birth=INFO['date_of_birth'],
            first_name='George',
            last_name='Doe',
            country=INFO['country'],
            city='London',
            address=INFO['address'],
            user_type=User.UserType.PROFESSIONAL,
        )

        filter_query1 = Q(first_name__in=User.objects.filter(first_name=INFO['first_name']).values('first_name'))
        filter_query2 = User.objects.filter(filter_query1).values('first_name')

        final_list = []
        for user_dict in list(filter_query2):
            final_list.append(user_dict['first_name'])
        assert final_list == [user1.first_name, user2.first_name]

    def test_filter_by_last_name(self, create_user):
        user1 = create_user(
            phone_number='111111',
            password=INFO['password'],
            email='john.doe@example.com',
            date_of_birth=INFO['date_of_birth'],
            first_name=INFO['first_name'],
            last_name=INFO['last_name'],
            country=INFO['country'],
            city=INFO['city'],
            address=INFO['address'],
            user_type=User.UserType.CLIENT,
        )
        user2 = create_user(
            phone_number='222222',
            password=INFO['password'],
            email='john.doe2@example.com',
            date_of_birth=INFO['date_of_birth'],
            first_name=INFO['first_name'],
            last_name=INFO['last_name'],
            country=INFO['country'],
            city='Toronto',
            address=INFO['address'],
            user_type=User.UserType.CLIENT,
        )
        create_user(
            phone_number='333333',
            password=INFO['password'],
            email='john.doe2@example.com',
            date_of_birth=INFO['date_of_birth'],
            first_name='George',
            last_name='Doe',
            country=INFO['country'],
            city='London',
            address=INFO['address'],
            user_type=User.UserType.PROFESSIONAL,
        )

        filter_query1 = Q(last_name__in=User.objects.filter(last_name=INFO['last_name']).values('last_name'))
        filter_query2 = User.objects.filter(filter_query1).values('last_name')

        final_list = []
        for user_dict in list(filter_query2):
            final_list.append(user_dict['last_name'])
        assert final_list == [user1.last_name, user2.last_name]

    def test_filter_by_city(self, create_user):
        user = create_user(
            phone_number='111111',
            password=INFO['password'],
            email='john.doe@example.com',
            date_of_birth=INFO['date_of_birth'],
            first_name='John',
            last_name='Doe',
            country=INFO['country'],
            city=INFO['city'],
            address=INFO['address'],
            user_type=User.UserType.CLIENT,
        )
        create_user(
            phone_number='222222',
            password=INFO['password'],
            email='john.doe2@example.com',
            date_of_birth=INFO['date_of_birth'],
            first_name='Jane',
            last_name='Doe',
            country=INFO['country'],
            city='Toronto',
            address=INFO['address'],
            user_type=User.UserType.CLIENT,
        )
        create_user(
            phone_number='333333',
            password=INFO['password'],
            email='john.doe2@example.com',
            date_of_birth=INFO['date_of_birth'],
            first_name='George',
            last_name='Doe',
            country=INFO['country'],
            city='London',
            address=INFO['address'],
            user_type=User.UserType.PROFESSIONAL,
        )

        filter_query1 = Q(phone_number__in=User.objects.filter(city=INFO['city']).values('phone_number'))
        filter_query2 = User.objects.filter(filter_query1).values('phone_number')
        assert list(filter_query2)[0] == {'phone_number': user.phone_number}
