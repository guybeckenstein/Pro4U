from django.urls import path
from . import views


urlpatterns = [
    path('typeOfJob/', views.jobs_list, name='jobs'),
    path('typeOfJob/create/', views.create_job, name='typeOfJob_create'),
    path('typeOfJob/update/<int:pk>/', views.TypeOfJobUpdate.as_view(), name='typeOfJob_update'),
    path('typeOfJob/delete/<int:pk>/', views.type_of_job_delete, name='typeOfJob_delete'),
    path("calendar/", views.CalendarView.as_view(user=False), name="calendar"),
    path("make-Appointment/<int:pk>/", views.CalendarView.as_view(user=True), name="make_appointment"),
    path("confirm-Appointment/<int:professional_id>/<int:day>:<int:month>:<int:year>/<str:meeting>/",
         views.confirm_appointment, name="confirm_appointment"),
    path('my-appointments/', views.appointment_list, name='my_appointments'),
    path('appointment/delete/<int:pk>/', views.appointment_delete, name='appointment_delete'),
    path("schedule_new/", views.create_schedule, name="schedule_new"),
    path("schedule/<int:schedule_id>/details/", views.schedule_details, name="schedule_detail"),
    path("schedule/edit/<int:pk>/", views.ScheduleEdit.as_view(), name="schedule_edit"),
    path("schedule/<int:pk>/remove", views.ScheduleDeleteView.as_view(), name="remove_schedule"),
]
