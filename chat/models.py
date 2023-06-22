from django.db import models
from django.utils import timezone
from account.models.professional import Professional
from account.models.user import User


class Message(models.Model):

    class SenderType(models.IntegerChoices):
        CLIENT = 1
        PROFESSIONAL = 2

    id = models.BigAutoField(primary_key=True, verbose_name="ID")
    sender_type = models.PositiveSmallIntegerField(choices=SenderType.choices)
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        db_table = 'Message'

    def __str__(self):
        if self.sender_type == 1:
            return f'From: ({self.user}). To: ({self.professional}). Time: {self.date}'
        elif self.sender_type == 2:
            return f'From: ({self.professional}). To: ({self.user}). Time: {self.date}'
        else:
            raise ValueError

    @staticmethod
    def filter_chats_by_professional(professional):
        return list({message.user for message in Message.objects.filter(professional=professional)})

    @staticmethod
    def filter_chats_by_user(user):
        return list({message.professional for message in Message.objects.filter(user=user)})

    @staticmethod
    def filter_chat_by_professional_and_user(professional, user):
        return Message.objects.filter(professional=professional, user=user)
