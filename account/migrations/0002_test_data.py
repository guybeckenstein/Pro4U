from account.models.user import User
from account.models.professional import Professional

import datetime
from django.db import migrations, transaction


class Migration(migrations.Migration):
    dependencies = [
        ('account', '0001_initial'),
    ]

    def generate_professionals_data(apps, schema_editor):
        test_data = [
            (
                111111111, 'TalPassword', 'tal@email.com',
                'Tal', 'Reinfeld', 'Israel', 'Tel Aviv',
                Professional.Professions.Handyman
            ),
            (
                222222222, 'TalPassword', 'ido@email.com',
                'Ido', 'Singer', 'Israel', 'Rishon',
                Professional.Professions.Handyman
            ),
            (
                333333333, 'Ido2Password', 'ido2@email.com',
                'Ido', 'Yekutiel', 'Israel', 'Tel Aviv',
                Professional.Professions.Plumber
            ),
            (
                444444444, 'PatPassword', 'pat@email.com',
                'Patrisia', 'Kaplun', 'Israel', 'Netanya',
                Professional.Professions.Electrician
            ),
            (
                555555555, 'OfirPassword', 'ofir@email.com',
                'Ofir', 'Bachar', 'Israel', 'Tel Aviv',
                Professional.Professions.Handyman
            ),
            (
                666666666, 'GuyPassword', 'guy@email.com',
                'Guy', 'Beckenstein', 'Israel', 'Givatayim',
                Professional.Professions.Electrician
            )
        ]
        with transaction.atomic():
            for (phone_number, password, email, first_name, last_name, country, city, profession) in test_data:
                user = User.objects.create_user(
                    phone_number=phone_number,
                    password=password,
                    email=email,
                    date_of_birth=datetime.datetime.now(),
                    image=f'/profile_pics/{first_name}{last_name}.jpg',
                    type=User.UserType.PROFESSIONAL,

                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    city=city,
                    address='Address',
                )
                professional = Professional(user=user, profession=profession)
                professional.save()

    def generate_clients_data(apps, schema_editor):
        test_data = [
            (
                7777777777, 'C1Password', 'Client1@email.com',
                'Client1', 'Client1', 'Israel', 'Tel Aviv'
            ),
            (
                8888888888, 'C2Password', 'Client2@email.com',
                'Client2', 'Client2', 'Israel', 'Netanya'
            ),
            (
                9999999999, 'C3Password', 'Client3@email.com',
                'Client3', 'Client3', 'Israel', 'Tel Aviv'
            ),
        ]
        with transaction.atomic():
            for (phone_number, password, email, first_name, last_name, country, city) in test_data:
                user = User.objects.create_user(
                    phone_number=phone_number,
                    password=password,
                    email=email,
                    date_of_birth=datetime.datetime.now(),
                    type=User.UserType.CLIENT,

                    first_name=first_name,
                    last_name=last_name,
                    country=country,
                    city=city,
                    address='Address',
                ).save()

    operations = [
        migrations.RunPython(generate_professionals_data),
        migrations.RunPython(generate_clients_data),
    ]
