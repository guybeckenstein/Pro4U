import pytest

import account.models.professional
from account.models import User
from conftest import BIRTHDAY
from review.models import Review

TEST_DATA = [
    ('3', 'Creating a test review', 0),
    ('2', 'Creating a test review', 200),
]


@pytest.mark.django_db
class TestReviewManager:
    def test_sort_review_by_oldest(self, create_user, create_professional, create_review):
        professional = self.create_reviews(create_user, create_professional, create_review)
        # Test sorting sorted_reviews by date (the oldest first)
        sorted_reviews = Review.objects.sort_review_by_oldest(professional=professional)
        self.assert_review(sorted_reviews.first(), rating=Review.Rating.TWO_STARS,
                           client_full_name='John Doe',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating='3',
                           client_full_name='John Doe',
                           professional_full_name='Bob Builder')

    def test_sort_review_by_newest(self, create_user, create_professional, create_review):
        professional = self.create_reviews(create_user, create_professional, create_review)
        # Test sorting sorted_reviews by date (the newest first)
        sorted_reviews = Review.objects.sort_review_by_newest(professional=professional)
        self.assert_review(sorted_reviews.first(), rating=Review.Rating.THREE_STARS,
                           client_full_name='John Doe',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating='2',
                           client_full_name='John Doe',
                           professional_full_name='Bob Builder')

    def test_sort_review_by_lowest_rating(self, create_user, create_professional, create_review):
        professional = self.create_reviews(create_user, create_professional, create_review)
        # Test sorting sorted_reviews by rating (the lowest first)
        sorted_reviews = Review.objects.sort_review_by_lowest_rating(professional=professional)
        self.assert_review(sorted_reviews.first(), rating='2',
                           client_full_name='John Doe',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating=Review.Rating.THREE_STARS,
                           client_full_name='John Doe',
                           professional_full_name='Bob Builder')

    def test_sort_review_by_highest_rating(self, create_user, create_professional, create_review):
        professional = self.create_reviews(create_user, create_professional, create_review)
        # Sort the sorted_reviews by highest rating and verify the first one has the highest rating.
        sorted_reviews = Review.objects.sort_review_by_highest_rating(professional=professional)
        self.assert_review(sorted_reviews.first(), rating='3',
                           client_full_name='John Doe',
                           professional_full_name='Bob Builder')
        self.assert_review(sorted_reviews.last(), rating=Review.Rating.TWO_STARS,
                           client_full_name='John Doe',
                           professional_full_name='Bob Builder')

    @staticmethod
    def create_reviews(create_user, create_professional, create_review) -> account.models.professional.Professional:
        user = create_user(
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
        )
        professional = create_professional()
        for fixture_num, (rating, description, days) in enumerate(TEST_DATA):
            if fixture_num + 1 == 1:
                create_review(rating, description, days, user, professional)
            else:
                create_review(rating, description, days, user, professional)
        return professional

    @staticmethod
    def assert_review(review, rating, client_full_name, professional_full_name):
        assert review.rating == rating
        assert f'{review.user.first_name} {review.user.last_name}' == client_full_name
        assert f'{review.professional.user.first_name} {review.professional.user.last_name}' == professional_full_name
