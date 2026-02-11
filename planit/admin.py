from django.contrib import admin
from .models import AppUser, Event, EventAttendance, EventImage

class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 3
    fields = ['image', 'caption', 'order']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'date_start', 'slots']
    inlines = [EventImageInline]

@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ['event', 'caption', 'uploaded_at', 'order']
    list_filter = ['event', 'uploaded_at']

admin.site.register(AppUser)
admin.site.register(EventAttendance)