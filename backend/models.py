from django.db import models
from django.conf import settings

class UserData(models.Model):
  user = models.OneToOneField(settings.AUTH_USER_MODEL)
  google_key = models.CharField(blank=True, null=True)
  up_key = models.CharField(blank=True, null=True)
  is_admin = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="is_admin")
