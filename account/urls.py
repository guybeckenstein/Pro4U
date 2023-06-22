from django.urls import path
from django.contrib.auth.views import LogoutView
from account.views import profile_views
from account.views import guest_views

urlpatterns = [
    # Not signed-in user actions
    path('register/', guest_views.register, name='register'),
    path('check-phone', guest_views.check_phone, name='check-phone'),
    path('check-password', guest_views.check_password, name='check-password'),
    path('check-first-name', guest_views.check_first_name, name='check-first-name'),
    path('check-last-name', guest_views.check_last_name, name='check-last-name'),
    path('check-country', guest_views.check_country, name='check-country'),
    path('check-city', guest_views.check_city, name='check-city'),

    path('login/', guest_views.sign_in, name='login'),
    # Professional
    path('profile/professional/<int:ID>/', profile_views.business_page, name='business_page'),
    # Profile
    path('profile/', profile_views.landing, name='profile_landing'),
    path('profile/professional/<int:ID>/', profile_views.business_page, name='show-professional'),
    path('profile/settings/', profile_views.settings, name='profile_settings'),
    path('profile/edit/', profile_views.update_profile, name='profile_edit'),
    path('logout/', LogoutView.as_view(), name='logout')

]
