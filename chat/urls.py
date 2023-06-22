from django.urls import path
from . import views


urlpatterns = [
    path('chat/<int:contact_id>/', views.chat, name='chat_message'),
    path('chat/', views.all_chats, name='all_chats')
    ]
