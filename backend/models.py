from django.db import models
from django.conf import settings

class UserData(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  google_key = models.CharField(blank=True, null=True, max_length=200)
  up_key = models.CharField(blank=True, null=True, max_length=200)

class CalendarEvent(models.Model):
  name = models.CharField(blank=True, null=True, max_length=200)
  start_date = models.DateTimeField(blank=True, null=True)
  end_date = models.DateTimeField(blank=True, null=True)
  description = models.TextField(blank=True, null=True)
  is_suggestion = models.BooleanField(default=False)
  user = models.ManyToManyField(UserData, related_name="events")