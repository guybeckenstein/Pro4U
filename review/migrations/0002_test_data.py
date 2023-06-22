from datetime import timedelta

from django.db import migrations, transaction
from django.utils import timezone

from account.models.user import User
from account.models.professional import Professional


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
        ('account', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from review.models import Review

        now = timezone.now()

        # Generate review data
        review_test_data = [
            (
                '5', 'Excellent!', now - timedelta(days=10),
                User.objects.filter(phone_number='111111111').first(),
                Professional.get_professional_by_phone_number('111111111').first(),
            ),
            (
                '4', 'Good', now - timedelta(days=20),
                User.objects.filter(phone_number='222222222').first(),
                Professional.get_professional_by_phone_number('222222222').first(),
            ),
            (
                '3', 'Average', now - timedelta(days=5),
                User.objects.filter(phone_number='333333333').first(),
                Professional.get_professional_by_phone_number('333333333').first(),
            ),
            (
                '2', 'A simple test review', now - timedelta(days=2),
                User.objects.filter(phone_number='111111111').first(),
                Professional.get_professional_by_phone_number('333333333').first(),
            ),
            (
                Review.Rating.FOUR_STARS, 'Another test review', now - timedelta(days=2),
                User.objects.filter(phone_number='333333333').first(),
                Professional.get_professional_by_phone_number('222222222').first(),
            ),
            (
                Review.Rating.ONE_STAR, 'Really bad.', now - timedelta(days=2),
                User.objects.filter(phone_number='444444444').first(),
                Professional.get_professional_by_phone_number('222222222').first(),
            ),
        ]
        # Create review
        with transaction.atomic():
            for rating, description, date_posted, user, professional in review_test_data:
                Review(
                    rating=rating,
                    description=description,
                    date_posted=date_posted,
                    user=user,
                    professional=professional
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
