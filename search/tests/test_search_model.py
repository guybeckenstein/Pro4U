from account.models import User
from conftest import USER_INFORMATION, BIRTHDAY
from search.models import Search
import pytest

EXPECTED_RESULT = 5


@pytest.fixture
def get_saved_search_instance(create_professional, create_user, create_search_instance):
    user = create_user(
        phone_number=USER_INFORMATION.get('phone_number')[0],
        password=USER_INFORMATION.get('password')[0],
        email=USER_INFORMATION.get('email')[0],
        date_of_birth=BIRTHDAY,

        first_name=USER_INFORMATION.get('first_name')[0],
        last_name=USER_INFORMATION.get('last_name')[0],
        country=USER_INFORMATION.get('country')[0],
        city=USER_INFORMATION.get('city')[0],
        address=USER_INFORMATION.get('address')[0],
        user_type=User.UserType.CLIENT
    )
    professional = create_professional(
        phone_number=USER_INFORMATION.get('phone_number')[2],
        password=USER_INFORMATION.get('password')[2],
        email=USER_INFORMATION.get('email')[2],

        user_type=User.UserType.PROFESSIONAL
    )
    search_instance = create_search_instance(user=user, professional=professional)
    search_instance.save()
    return search_instance


@pytest.mark.django_db
class TestSearchModel:
    def test_create_search_instance(self, create_user, create_professional, create_search_instance):
        user = create_user(
            phone_number=USER_INFORMATION.get('phone_number')[0],
            password=USER_INFORMATION.get('password')[0],
            email=USER_INFORMATION.get('email')[0],
            date_of_birth=BIRTHDAY,

            first_name=USER_INFORMATION.get('first_name')[0],
            last_name=USER_INFORMATION.get('last_name')[0],
            country=USER_INFORMATION.get('country')[0],
            city=USER_INFORMATION.get('city')[0],
            address=USER_INFORMATION.get('address')[0],
            user_type=User.UserType.CLIENT
        )
        professional = create_professional(
            phone_number=USER_INFORMATION.get('phone_number')[2],
            password=USER_INFORMATION.get('password')[2],
            email=USER_INFORMATION.get('email')[2],

            user_type=User.UserType.PROFESSIONAL
        )
        search_instance = create_search_instance(user=user, professional=professional)
        assert search_instance.user == user
        assert search_instance.professional == professional

    def test_save_search_instance(self, get_saved_search_instance):
        assert get_saved_search_instance in Search.objects.all()

    def test_delete_search_instance(self, get_saved_search_instance):
        search = get_saved_search_instance
        search.delete()
        assert search not in Search.objects.all()

    def test_filter_searches_by_user_and_professional(self, get_saved_search_instance):
        search_instance = get_saved_search_instance
        assert [search_instance] == list(Search.filter_searches_by_user_and_professional(
            user=search_instance.user,
            professional=search_instance.professional
        ))

    def test_get_last_professionals_search_by_client(self, get_saved_search_instance):
        user = get_saved_search_instance.user
        expected_professionals = list(Search.objects.filter(user=user).order_by('-date')[:EXPECTED_RESULT])
        result = Search.get_last_professionals_search_by_client(user=user, expected_result=EXPECTED_RESULT)
        assert sorted(result) == sorted(expected_professionals)
