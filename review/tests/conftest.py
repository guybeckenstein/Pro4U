from datetime import timedelta
from typing import Callable

import pytest
from django.utils import timezone

from account.models.user import User
from conftest import USER_INFORMATION, BIRTHDAY
from review.models import Review

DESCRIPTION = 'Creating a test review'
DAYS = 50
RATING = ['4', '1', '5']


@pytest.fixture(scope='function')
def create_review() -> Callable[[str, str, str, str, int], Review]:
    def _review_factory(rating: str, description: str, days: int, user: User, professional: str) -> Review:
        review = Review.objects.create(
            rating=rating,
            description=description,
            date_posted=timezone.now() - timedelta(days=days),
            user=user,
            professional=professional
        )
        return review

    return _review_factory


@pytest.fixture
def get_saved_review(create_user, create_professional, create_review):
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
    review = create_review(rating=RATING[0], description=DESCRIPTION, days=DAYS, user=user, professional=professional)
    review.save()
    return review
