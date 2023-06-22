from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('chat', '0001_initial'),
        ('account', '0002_test_data'),
    ]

    def generate_data(apps, schema_editor):
        from chat.models import Message
        from account.models.user import User
        from account.models.professional import Professional

        test_data = [
            (
                Message.SenderType.CLIENT,
                Professional.get_professional_by_phone_number('222222222').first(),
                User.objects.filter(phone_number='333333333').first(),
                'A simple test message1'
            ),
            (
                Message.SenderType.CLIENT,
                Professional.get_professional_by_phone_number('222222222').first(),
                User.objects.filter(phone_number='333333333').first(),
                'A simple test message2'
            ),
            (
                Message.SenderType.PROFESSIONAL,
                Professional.get_professional_by_phone_number('222222222').first(),
                User.objects.filter(phone_number='333333333').first(),
                'A simple test message3'
            ),
            (
                Message.SenderType.PROFESSIONAL,
                Professional.get_professional_by_phone_number('222222222').first(),
                User.objects.filter(phone_number='333333333').first(),
                'A simple test message4'
            ),
        ]

        with transaction.atomic():
            for sender_type, professional, user, content in test_data:
                Message(sender_type=sender_type, professional=professional, user=user, content=content).save()

    operations = [
        migrations.RunPython(generate_data),
    ]
