from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from PIL import Image

IMG_SIZE = 256


class UserCustomManager(BaseUserManager):

    use_in_migrations = True

    def _create_user(self, phone_number, password, **extra_fields):
        if not phone_number:
            raise ValueError('The given phone number must be set')
        user = self.model(phone_number=phone_number, username=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone_number, password, **extra_fields)

    def create_superuser(self, phone_number, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True.')

        return self._create_user(phone_number, password, **extra_fields)


class User(AbstractUser):
    class UserType(models.IntegerChoices):
        CLIENT = 1
        PROFESSIONAL = 2

    phone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(unique=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    data_join = models.DateTimeField(default=timezone.now)
    type = models.PositiveSmallIntegerField(choices=UserType.choices, default=UserType.CLIENT)

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    country = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=30, blank=True, null=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []


    objects = UserCustomManager()

    class Meta:
        db_table = 'User'
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def __str__(self):
        full_name = str(self.first_name) + ' ' + str(self.last_name)
        return f'{self.phone_number} | {self.email} | {full_name}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        image = Image.open(self.image.path)
        if (image.height > IMG_SIZE) or (image.width > IMG_SIZE):
            output_size = (IMG_SIZE, IMG_SIZE)
            image.thumbnail(output_size)
            image.save(self.image.path)
