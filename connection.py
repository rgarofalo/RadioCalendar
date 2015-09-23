import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'RadioCalendar'

palinsestoId ='xxxxxxxx@group.calendar.google.com'

class connection():
   
    def get_credentials(self):

    	home_dir = os.path.expanduser('~')
    	credential_dir = os.path.join(home_dir, '.credentials')

    	if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)

        credential_path = os.path.join(credential_dir,'calendar-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()

        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            if flags:
                credentials = tools.run_flow(flow, store, flags)
            else: # Needed only for compatability with Python 2.6
                credentials = tools.run(flow, store)
            print 'Storing credentials to ' + credential_path
        return credentials

    def insert_calendar_events(self,calendar_events, service):
        count = 0
        for event in calendar_events:
            print event
            count += 1
            print count
            try:
              # The Calendar API's events().list method returns paginated results, so we
              # have to execute the request in a paging loop. First, build the
              # request object. The arguments provided are:
              #   primary calendar for user
              # request = service.events().list(calendarId='primary')
              # # Loop until all pages have been processed.
              # while request != None:
              #   # Get the next page.
              #   response = request.execute()
              #   # Accessing the response like a dict object with an 'items' key
              #   # returns a list of item objects (events).
              #   for event in response.get('items', []):
              #     # The event object is a dict object with a 'summary' key.
              #     print repr(event.get('summary', 'NO SUMMARY')) + '\n'
              #   # Get the next request object by passing the previous request object to
              #   # the list_next method.
              #   request = service.events().list_next(request, response)
                  created_event = service.events().insert(calendarId=palinsestoId, body=event).execute()
                  print created_event['id']

            except ValueError:
              # The AccessTokenRefreshError exception is raised if the credentials
              # have been revoked by the user or they have expired.
              # Could not load Json body.
              
              print 'HTTP Status code: %d' % e.resp.status
              print 'HTTP Reason: %s' % e.resp.reason

    def clearCalendar(self,service):

      eventsResult = service.events().list(calendarId=palinsestoId).execute()

      for event in eventsResult['items']:
        service.events().delete(calendarId=palinsestoId, eventId=event['id']).execute()

      return


