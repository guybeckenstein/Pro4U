from django.db import migrations, transaction
from datetime import timedelta
from django.utils import timezone

from account.models.user import User
from account.models.professional import Professional


class Migration(migrations.Migration):
    dependencies = [
        ('reservation', '0001_initial'),
        ('account', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from reservation.models import Schedule, Appointment, PriceList

        current_datetime = timezone.now()
        schedule_test_data = [
            (
                1,
                (current_datetime + timedelta(days=3)).replace(hour=14, minute=0, second=0, microsecond=0),
                (current_datetime + timedelta(days=3)).replace(hour=19, minute=0, second=0, microsecond=0),
                60
            ),
            (
                1,
                (current_datetime + timedelta(days=5)).replace(hour=14, minute=0, second=0, microsecond=0),
                (current_datetime + timedelta(days=5)).replace(hour=20, minute=0, second=0, microsecond=0),
                60
            ),
            (
                2,
                (current_datetime + timedelta(days=3)).replace(hour=14, minute=0, second=0, microsecond=0),
                (current_datetime + timedelta(days=3)).replace(hour=19, minute=0, second=0, microsecond=0),
                60
            ),
            (
                2,
                (current_datetime + timedelta(days=5)).replace(hour=14, minute=0, second=0, microsecond=0),
                (current_datetime + timedelta(days=5)).replace(hour=20, minute=0, second=0, microsecond=0),
                60
            ),
        ]

        price_list_test_data = [
            (1, "man haircut", 70),
            (1, "woman haircut", 100),
            (2, "Gel nail polish", 80),
        ]

        appointment_test_data = [
            (1, 2, 2, (current_datetime + timedelta(days=3)).replace(hour=15, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=3)).replace(hour=16, minute=0, second=0, microsecond=0), ""),
            (3, 2, 2, (current_datetime + timedelta(days=3)).replace(hour=16, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=3)).replace(hour=17, minute=0, second=0, microsecond=0), ""),
            (2, 1, 1, (current_datetime + timedelta(days=3)).replace(hour=18, minute=0, second=0, microsecond=0),
             (current_datetime + timedelta(days=3)).replace(hour=19, minute=0, second=0, microsecond=0), ""),
        ]

        with transaction.atomic():
            for ID, (professional, start_day, end_day, meeting_time) in enumerate(schedule_test_data):
                Schedule(
                    id=ID + 1,
                    professional=Professional.objects.get(pk=professional),
                    start_day=start_day,
                    end_day=end_day,
                    meeting_time=meeting_time
                ).save()

            for ID, (professional, job_name, price) in enumerate(price_list_test_data):
                PriceList(
                    id=ID + 1,
                    professional=Professional.objects.get(pk=professional),
                    job_name=job_name,
                    price=price
                ).save()

            for ID, (professional, user, job, start, end, summary) in enumerate(appointment_test_data):
                Appointment(
                    id=ID + 1,
                    professional=Professional.objects.get(pk=professional),
                    user=User.objects.get(pk=user),
                    job=PriceList.objects.get(pk=job),
                    start=start,
                    end=end,
                    summary=summary
                ).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
