from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('search', '0001_initial'),
        ('account', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from search.models import Search
        from account.models.user import User
        from account.models.professional import Professional

        test_data = [
            (
                '1',
                User.objects.filter(phone_number='333333333').first(),
                Professional.get_professional_by_phone_number('222222222').first(),
            ),
            (
                '2',
                User.objects.filter(phone_number='333333333').first(),
                Professional.get_professional_by_phone_number('222222222').first(),
            ),
            (
                '3',
                User.objects.filter(phone_number='333333333').first(),
                Professional.get_professional_by_phone_number('222222222').first(),
            ),
            (
                '4',
                User.objects.filter(phone_number='333333333').first(),
                Professional.get_professional_by_phone_number('222222222').first(),
            ),
        ]

        with transaction.atomic():
            for ID, user, professional in test_data:
                Search(id=ID, user=user, professional=professional).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
