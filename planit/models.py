from django.db import models

class AppUser(models.Model):
    name = models.CharField (verbose_name="Name", max_length=50, default='')
    last_name = models.CharField (verbose_name="Last Name", max_length=100, default='')
    email = models.CharField (verbose_name="E-Mail", max_length=200, default='', unique=True)
    password = models.CharField (verbose_name="Password", default='')
    telephone = models.CharField (verbose_name="Telephone Number", max_length=20, default='', unique=True)
    age = models.PositiveSmallIntegerField (verbose_name="Age", default=0)
    
    class Meta:
        verbose_name = "App User"
        verbose_name_plural = "App Users"
        
    def __str__(self):
        return f'{self.name} {self.last_name}'

class Event (models.Model):
    title = models.CharField (verbose_name="Title", max_length=100, default='')
    description = models.CharField (verbose_name="Description", max_length=1000, default='')
    location = models.CharField (verbose_name="Event Location", max_length=200, default='')
    slots = models.PositiveIntegerField (verbose_name="Available Slots", default=0)
    date_created = models.DateTimeField(verbose_name="Date of Creation", auto_now_add=True)
    date_start = models.DateTimeField(verbose_name="Date of Event")
    
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

class EventAttendance(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    regdate = models.DateTimeField(verbose_name="Registered Date", auto_now_add=True)
    
    class Meta:
        unique_together = ['user','event']
        verbose_name = "Event Attendance"
        verbose_name_plural = "Event Attendances"