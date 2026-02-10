from django.contrib import admin
from planit.models import AppUser,Event,EventAttendance

admin.site.register(AppUser)
admin.site.register(Event)
admin.site.register(EventAttendance)