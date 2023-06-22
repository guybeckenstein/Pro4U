from django.contrib import admin
from .models import PriceList, Appointment, Schedule

admin.site.register(PriceList)
admin.site.register(Appointment)
admin.site.register(Schedule)
