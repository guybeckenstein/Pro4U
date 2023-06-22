from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('learn-more/', views.learn_more, name='learn_more'),
]
