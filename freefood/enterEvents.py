from backend.models import *
from freefood.testCalendar import getEvents
from django.contrib.auth.models import User

timeFormat = "%d-%d-%dT00:00:00+00:00" # % (year, month, day)

def enterEvents(username, sY, sM, sD, eY, eM, eD):
  user = User.objects.get(username = username)
  userdata = user.userdata
  start = timeFormat % (sY, sM, sD)
  end = timeFormat % (eY, eM, eD)
  events = getEvents(start, end)
  for (name, startTime, endTime) in events:
    print name
    event = CalendarEvent(name = name, start_date = startTime, end_date = endTime,
      is_suggestion=False)
    event.save()
    event.user.add(userdata)