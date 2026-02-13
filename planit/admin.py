from django.contrib import admin
from .models import AppUser, Event, EventAttendance, EventImage

#   --- EVENT IMAGE INLINE - Interfaz de Edición
#       --- Interfaz creada para la gestión de
#       --- imágenes de Evento mediante el
#       --- Sistema de Administración de Django
class EventImageInline(admin.TabularInline):
    model = EventImage
    extra = 3
    fields = ['image', 'caption', 'order']

#   --- REGISTRO DE MODELOS ADMIN

#   --- --- EVENT
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'date_start', 'slots']
    inlines = [EventImageInline]
    
#   --- --- EVENT IMAGE
@admin.register(EventImage)
class EventImageAdmin(admin.ModelAdmin):
    list_display = ['event', 'caption', 'uploaded_at', 'order']
    list_filter = ['event', 'uploaded_at']

#   --- --- APP USER
admin.site.register(AppUser)

#   --- --- EVENT ATTENDANCE
admin.site.register(EventAttendance)