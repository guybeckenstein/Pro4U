import pytest
from review.models import Review


@pytest.mark.django_db
class TestReviewManager:
    def test_sort_review_by_oldest(self) -> None:
        # Test sorting sorted_reviews by date (the oldest first)
        sorted_reviews = Review.objects.sort_review_by_oldest()
        self.assert_review(sorted_reviews.first(), rating='4',
                           client_full_name='Client2 Client2',
                           professional_full_name='Ido Singer')
        self.assert_review(sorted_reviews.last(), rating='2',
                           client_full_name='Client1 Client1',
                           professional_full_name='Ido2 Yekutiel')

    def test_sort_review_by_newest(self) -> None:
        # Test sorting sorted_reviews by date (the newest first)
        sorted_reviews = Review.objects.sort_review_by_newest()
        self.assert_review(sorted_reviews.first(), rating='2',
                           client_full_name='Client1 Client1',
                           professional_full_name='Ido2 Yekutiel')
        self.assert_review(sorted_reviews.last(), rating='4',
                           client_full_name='Client2 Client2',
                           professional_full_name='Ido Singer')

    def test_sort_review_by_lowest_rating(self) -> None:
        # Test sorting sorted_reviews by rating (the lowest first)
        sorted_reviews = Review.objects.sort_review_by_lowest_rating()
        self.assert_review(sorted_reviews.first(), rating='1',
                           client_full_name='Client3 Client3',
                           professional_full_name='Ido Singer')
        self.assert_review(sorted_reviews.last(), rating='5',
                           client_full_name='Client1 Client1',
                           professional_full_name='Tal Reinfeld')

    @pytest.mark.django_db
    def test_sort_review_by_highest_rating(self) -> None:
        # Sort the sorted_reviews by highest rating and verify the first one has the highest rating.
        sorted_reviews = Review.objects.sort_review_by_highest_rating()
        self.assert_review(sorted_reviews.first(), rating='5',
                           client_full_name='Client1 Client1',
                           professional_full_name='Tal Reinfeld')
        self.assert_review(sorted_reviews.last(), rating='1',
                           client_full_name='Client3 Client3',
                           professional_full_name='Ido Singer')

    @staticmethod
    def assert_review(review, rating, client_full_name, professional_full_name) -> None:
        client_user = review.client.profile_id.user_id
        professional_user = review.professional.profile_id.user_id
        assert review.rating == rating
        assert client_user.first_name + ' ' + client_user.last_name == client_full_name
        assert professional_user.first_name + ' ' + professional_user.last_name == professional_full_name
