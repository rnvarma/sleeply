from django.db import models
from django.conf import settings

class UserData(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  google_key = models.CharField(blank=True, null=True, max_length=100)
  up_key = models.CharField(blank=True, null=True, max_length=100)