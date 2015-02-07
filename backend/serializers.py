from rest_framework import serializers
from backend.models import *

class EventSerializer(serializers.ModelSerializer):
  class Meta:
    model = CalendarEvent
    fields = ('name', 'start_date', 'end_date', 'description', 'is_suggestion')