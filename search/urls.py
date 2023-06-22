from django.urls import path
from . import views

urlpatterns = [
    path('search/<int:ID>/', views.search, name='search-history'),
]
