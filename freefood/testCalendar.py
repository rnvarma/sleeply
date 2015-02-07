import gflags, httplib2, datetime

from googleapiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.tools import run


def getEvents(startRange,endRange):
  FLAGS = gflags.FLAGS

  # Set up a Flow object to be used if we need to authenticate. This
  # sample uses OAuth 2.0, and we set up the OAuth2WebServerFlow with
  # the information it needs to authenticate. Note that it is called
  # the Web Server Flow, but it can also handle the flow for native
  # applications
  # The client_id and client_secret are copied from the API Access tab on
  # the Google APIs Console
  FLOW = OAuth2WebServerFlow(
      client_id='196405873859-d2tuulj4imr0r5olf32mbdlcjat4hihm.apps.googleusercontent.com',
      client_secret='jPH7iuGvb2J2uYrR7qyCrrN1',
      scope='https://www.googleapis.com/auth/calendar',
      user_agent='sleeply/v1')

  # To disable the local server feature, uncomment the following line:
  # FLAGS.auth_local_webserver = False

  # If the Credentials don't exist or are invalid, run through the native client
  # flow. The Storage object will ensure that if successful the good
  # Credentials will get written back to a file.
  storage = Storage('calendar.dat')
  credentials = storage.get()
  if credentials is None or credentials.invalid == True:
    credentials = run(FLOW, storage)

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with our good Credentials.
  http = httplib2.Http()
  http = credentials.authorize(http)

  # Build a service object for interacting with the API. Visit
  # the Google APIs Console
  # to get a developerKey for your own application.
  service = build(serviceName='calendar', version='v3', http=http,
         developerKey='AIzaSyDRD1yDR9Cxp0uyknrmPTW_arcSp3lUl_g')


  calendar = service.calendars().get(calendarId='primary').execute()
  events = service.events().list(calendarId='primary', timeMin=startRange, timeMax=endRange).execute()
  # print events
  currentEvents = []
  dateFormat = "%Y-%m-%dT%H:%M:%S"
  for event in events['items']:
    try:
      eventTitle = event['summary']
      startField = event['start']
      endField = event['end']
      startIdx = startField['dateTime'].rfind('-')
      endIdx = endField['dateTime'].rfind('-')
      start = startField['dateTime'][:startIdx]
      end = endField['dateTime'][:endIdx]
      startTime = datetime.datetime.strptime(start,dateFormat)
      endTime = datetime.datetime.strptime(end,dateFormat)
      currentEvents.append((eventTitle,startTime,endTime))
    except:
      print event
  return currentEvents

