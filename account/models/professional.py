from django.db import models
from .user import User


class Professional(models.Model):
    class Professions(models.TextChoices):
        Plumber = 'PLU', 'Plumber'
        Gardener = 'GAR', 'Gardener'
        Electrician = 'ELE', 'Electrician'
        Tinsmith = 'TIN', 'Tinsmith'
        Painter = 'PAI', 'Painter'
        Locksmith = 'LOC', 'Locksmith'
        Exterminator = 'EXT', 'Exterminator'
        GasTechnician = 'GAT', 'GasTechnician'
        AirConditioningTechnician = 'ACT', 'AirConditioningTechnician'
        RefrigeratorTechnician = 'RET', 'RefrigeratorTechnician'
        Cleaner = 'CLE', 'Cleaner'
        Handyman = 'HAN', 'Handyman'

    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    user: User = models.OneToOneField(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=3, choices=Professions.choices)

    class Meta:
        db_table = 'Professional'

    def __str__(self):
        return f'{self.user} | {self.get_profession_display()}'

    def get_phone_number(self):
        return self.user.phone_number

    def get_email(self):
        return self.user.email

    def get_first_name(self):
        return self.user.first_name

    def get_last_name(self):
        return self.user.last_name

    @staticmethod
    def get_professional_by_phone_number(phone_number):
        return Professional.objects.filter(user__phone_number=phone_number)
