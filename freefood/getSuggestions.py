import datetime
from backend.models import *
from freefood.jawbone import regular, allnighter
from django.contrib.auth.models import User


def filterEvents(username, lower, upper):
  user = User.objects.get(username = username)
  events = user.userdata.events.all()
  def filterDates(event):
    d1 = event.start_date.replace(tzinfo=None)
    return lower <= d1 <= upper
  filteredEvents = map(lambda x: (x.start_date.replace(tzinfo=None), x.end_date.replace(tzinfo=None)),
                       filter(filterDates, events))
  return filteredEvents

def enterEvents(username, eventList):
  user = User.objects.get(username = username)
  userdata = user.userdata
  def mapEntries(event):
    event = CalendarEvent(name = event['title'], start_date = event['startTime'],
      end_date = event['endTime'], is_suggestion=True)
    event.save()
    event.user.add(userdata)
  map(mapEntries, eventList)

def getRegularSuggestions(username, start_sunday):
  lower = start_sunday
  upper = start_sunday + datetime.timedelta(days=7)
  filteredEvents = filterEvents(username, lower, upper)
  result = [[] for i in xrange(7)]

  for (start, end) in filteredEvents:
    delta = start - start_sunday
    i = delta.days
    if i <= 6:
      result[i].append((start,end))
  return regular("", result)

def getHackathonSuggestions(username, date):
  lower = datetime.datetime.today()
  upper = lower + datetime.timedelta(days = 3)
  filteredEvents = filterEvents(username, lower, upper)
  return allnighter("", filteredEvents, date)





