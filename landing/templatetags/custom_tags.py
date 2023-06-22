from django import template
from django.core.exceptions import ObjectDoesNotExist

from account.models.user import User
from account.models.professional import Professional

register = template.Library()


@register.filter
def retrieve_user_by_phone_number(user: User):
    try:
        user_instance = User.objects.get(phone_number=user.phone_number)
        return user_instance
    except ObjectDoesNotExist:
        return None


@register.filter
def retrieve_professional_by_phone_number(user: User):
    try:
        professional_instance = Professional.objects.get(user__phone_number=user.phone_number)
        return professional_instance
    except ObjectDoesNotExist:
        return None
