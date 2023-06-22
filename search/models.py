from django.db import models
from django.utils import timezone

from account.models.user import User
from account.models.professional import Professional


class Search(models.Model):
    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Search'

    def __str__(self):
        return f'Client ({self.user}) searched ({self.professional}) on: {self.date}'

    @staticmethod
    def filter_searches_by_user_and_professional(user, professional):
        return Search.objects.filter(user=user, professional=professional)

    @staticmethod
    def get_last_professionals_search_by_client(user, expected_result=5):
        return Search.objects.filter(user=user).order_by('-date')[:expected_result]
