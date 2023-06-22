import pytest

from account.models import User
from conftest import BIRTHDAY
from review.models import Review
from django.template.backends import django

from review.tests.conftest import RATING, DESCRIPTION, DAYS


@pytest.mark.django_db
class TestReview:
    def test_get_new_review(self, get_saved_review):
        review = get_saved_review
        assert review in Review.objects.all()

    def test_get_deleted_review(self, get_saved_review):
        review = get_saved_review
        Review.objects.filter(id=review.id).delete()
        assert review not in Review.objects.all()

    def test_method_filter_by_professional(self, get_saved_review):
        review = get_saved_review
        filtered_reviews = Review.filter_by_professional(professional=review.professional)
        filtered_reviews_lst = list(filtered_reviews)

        if isinstance(review, Review):
            assert filtered_reviews_lst == [review]
        elif isinstance(review, django.db.models.query.QuerySet):
            assert filtered_reviews_lst == [*review]
        else:
            error_msg = "review type is neither Review or django.db.models.query.QuerySet"
            with pytest.raises(TypeError, match=error_msg):
                raise TypeError("review type is neither Review or django.db.models.query.QuerySet")

        assert len(filtered_reviews_lst) == 1

    def test_method_get_professional_avg_rating(self, create_user, create_professional, create_review):
        professional = create_professional()
        # We create new client instance in each tuple in `reviews_data`
        reviews_data = [
            (
                create_user(
                    phone_number='972541234',
                    password='123456',
                    email='john1@doe.com',
                    date_of_birth=BIRTHDAY,
                    user_type=User.UserType.CLIENT,

                    first_name='John',
                    last_name='Doe',
                    country='United Kingdom',
                    city='London',
                    address='Address'
                ),
                RATING[0]
            ),
            (
                create_user(
                    phone_number='972541232',
                    password='123456',
                    email='jane@doe.com',
                    date_of_birth=BIRTHDAY,
                    user_type=User.UserType.CLIENT,

                    first_name='Jane',
                    last_name='Doe',
                    country='United Kingdom',
                    city='London',
                    address='Address'
                ),
                RATING[1]
            ),
            (
                create_user(
                    phone_number='972641214',
                    password='123456',
                    email='george@doe.com',
                    date_of_birth=BIRTHDAY,
                    user_type=User.UserType.CLIENT,

                    first_name='George',
                    last_name='Doe',
                    country='United Kingdom',
                    city='London',
                    address='Address'
                ),
                RATING[2]
            ),
        ]

        for i, (user, rating) in enumerate(reviews_data):  # Using factory function within this loop
            create_review(rating, DESCRIPTION, DAYS, user, professional)
            if i == 1:  # Average of 2 review
                assert Review.get_professional_avg_rating(professional=professional) == 2.5

        review_rounded_avg_rating = round(Review.get_professional_avg_rating(professional=professional), 1)
        assert review_rounded_avg_rating == 3.3  # Average of `len(RATING)` reviews
