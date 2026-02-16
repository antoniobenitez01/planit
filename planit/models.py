from django.db import models
from django.contrib.auth.models import AbstractUser

#   --- APPUSER - Clase de Usuario
#   ---     Hereda de AbstractUser para hacer uso de sus funcionalidades
#   ---     de Usuario en el sistema de Administración de Django
class AppUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)  # Temporarily nullable
    telephone = models.CharField (verbose_name="Telephone Number", max_length=20, default='', unique=True)
    age = models.PositiveSmallIntegerField (verbose_name="Age", default=0)
    
    class Meta:
        verbose_name = "App User"
        verbose_name_plural = "App Users"
        
    def __str__(self):
        return f'{self.first_name} {self.last_name}' if self.first_name else self.username

#   --- EVENTO - Clase de Evento
#   ---     Contiene referencias ForeignKey y ManyToManyField
#   ---     en base al creador del Evento y a la gente que
#   ---     asistirá al Evento
class Event (models.Model):
    title = models.CharField (verbose_name="Title", max_length=100, default='')
    description = models.CharField (verbose_name="Description", max_length=1000, default='')
    location = models.CharField (verbose_name="Event Location", max_length=200, default='')
    slots = models.PositiveIntegerField (verbose_name="Available Slots", default=0)
    date_created = models.DateTimeField(verbose_name="Date of Creation", auto_now_add=True)
    date_start = models.DateTimeField(verbose_name="Date of Event")
    is_finished = models.BooleanField(default=False, verbose_name="Event Finished")
    
    creator = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name="created_events",
        verbose_name="Creator"
    )
    
    attendees = models.ManyToManyField(
        AppUser,
        related_name='attending_events',
        through='EventAttendance',
        blank=True
    )
    
    class Meta:
        verbose_name = "Event"
        verbose_name_plural = "Events"
    
    def __str__(self):
        return self.title
    
#   --- EVENT IMAGE - Clase de Imagen de Evento
#   ---     Creada con el propósito de facilitar
#   ---     la subida y eliminación de imágenes
#   ---     de las galerías de cada Evento
class EventImage(models.Model):
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Event"
    )
    image = models.ImageField(
        upload_to='event_images/%Y/%m/%d/',
        verbose_name="Image"
    )
    caption = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Caption"
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Uploaded At"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Display Order"
    )
    
    class Meta:
        verbose_name = "Event Image"
        verbose_name_plural = "Event Images"
        ordering = ['order', '-uploaded_at']
    
    def __str__(self):
        return self.caption if self.caption else f"Image for {self.event.title}"

#   --- EVENT ATTENDANCE - Clase auxiliar
#   ---     Representa la relación que implica
#   ---     asistir a un Evento junto a la fecha de registro
class EventAttendance(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    regdate = models.DateTimeField(verbose_name="Registered Date", auto_now_add=True)
    
    class Meta:
        unique_together = ['user','event']
        verbose_name = "Event Attendance"
        verbose_name_plural = "Event Attendances"