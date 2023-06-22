from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models.user import User
from account.models.professional import Professional
from .models import Message


@login_required
def chat(request, contact_id):

    professional = Professional.objects.filter(user=request.user).first()
    if professional:
        user = User.objects.get(id=contact_id)
        contacts = list({Message.filter_chats_by_professional(professional)})
        contact_name = user.first_name
        sender_type = Message.SenderType.PROFESSIONAL
    else:
        professional = Professional.objects.get(id=contact_id)
        user = User.objects.filter(phone_number=request.user).first()
        contacts = list(set(Message.filter_chats_by_user(user)))
        contact_name = professional.user.first_name
        sender_type = Message.SenderType.CLIENT

    context = {
            'chat': Message.filter_chat_by_professional_and_user(professional=professional, user=user),
            'contact_name': contact_name,
            'contacts': contacts,
            'sender_type': sender_type,
        }

    if request.method == "POST":
        content = request.POST.get("msg_sent", "")

        if content != '':
            Message(professional=professional, user=user, content=content, sender_type=sender_type).save()

        else:
            notification = "An empty message cannot be sent."
            context['notification'] = notification

    return render(request, 'chat/message.html', context)


@login_required
def all_chats(request):
    professional = Professional.objects.filter(user__phone_number=request.user).first()
    if professional:
        contacts = list(set(Message.filter_chats_by_professional(professional)))
        sender_type = Message.SenderType.PROFESSIONAL
        if contacts:
            return chat(request, contacts[0].user)

    else:
        user = User.objects.filter(phone_number=request.user).first()
        contacts = list(set(Message.filter_chats_by_user(user)))
        sender_type = Message.SenderType.CLIENT
        if contacts:
            return chat(request, contacts[0].professional)

    if not contacts:
        contact_name = ''

    context = {
        'chat': [],
        'contact_name': contact_name,
        'contacts': contacts,
        'sender_type': sender_type,
    }

    return render(request, 'chat/message.html', context)
