import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

from json import JSONDecoder
from urllib2 import urlopen

import time
import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'RadioCalendar'

palinsestoId ='xxxxxxxxx'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
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

def main():

    schedule = {'lu':[],'ma':[],'me':[],'gi':[],'ve':[],'sa':[],'do':[]}
    
    if updateSchedule(schedule):
      lis = build_calendar_events(schedule)
      #for e in lis:
       # print e
      
      
      credentials = get_credentials()
      http = credentials.authorize(httplib2.Http())
      service = discovery.build('calendar', 'v3', http=http)
      
      clearCalendar(service)

      insert_calendar_events(lis, service)
    else :
      print 'Aggionameto non necessario'

    
def updateSchedule(schedule): # This function will update the schedule
      
      days = ['lu','ma','me','gi','ve','sa','do'] 
      dec = JSONDecoder(encoding='ascii') 
      rawdata = urlopen('http://www.radiocicletta.it:80/programmi.json').read() # We retrieve the json in str type

      if os.path.isfile('programmi.txt'): 
        progfile= open("programmi.txt","r")
        old_program= progfile.read()
        progfile.close()
      else:
        old_program=""

      if old_program==rawdata:
        return False
      else:
        progfile = open('programmi.txt','w')
        progfile.write(rawdata)
        progfile.close()

        # Now we extract from string rawdata the list of programs active (stato == 1)
        listaProgs = filter(lambda x: x['stato'] == '1',dec.decode(rawdata)['programmi']) 
        
        # Finally insert in the dictionary schedule the list of start time of the programs
        minList=minimalList(listaProgs);
        for today in days:
           schedule[today] = filter(lambda t:t['title']!='Musica No Stop',filter(lambda x: x['start'][0] == today, minList)) 
        
        #print schedule

        return True

def minimalList(listaProgs):

  minList = []
  for prog in listaProgs:
    dictionary={'title':prog['title'],'start':prog['start'],'end':prog['end']}
    minList.append(dictionary)

  return minList



def insert_calendar_events(calendar_events, service):
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

def build_calendar_events(schedule): 
  event_list = []
  weekdays = ['lu','ma','me','gi','ve','sa','do']

  now = datetime.datetime.today()
  today = now.day
  weekday=now.weekday()

  for day in weekdays:
    for prog in schedule[day]:

      addDay=7 - weekday + weekdays.index(day)
      data= now + datetime.timedelta(days=addDay)

      #google vuole l'orario di greenwich
      if(prog['end'][1]==0):
        prog['end'][1]=23
      else:
        prog['end'][1] -=1

      if(prog['start'][1]==0):
        prog['start'][1]=23
      else:
        prog['start'][1] -=1

      endtime=str(prog['end'][1]).zfill(2) + ":"+str(prog['end'][2]).zfill(2)
      if endtime=='00:00':
        endtime='23:59'

      add_event = {
          'summary': prog['title'],
          'location': 'pisa',
          'start': {
            'dateTime': data.strftime("%Y-%m-%d") + "T" + str(prog['start'][1]).zfill(2) + ":"+str(prog['start'][2]).zfill(2)+":00+01:00",
            'timeZone': "Europe/Rome"
          },
          'end': {
            'dateTime': data.strftime("%Y-%m-%d") + "T" + endtime +":00+01:00",
            'timeZone': "Europe/Rome"
          },
           'recurrence': [
                     'RRULE:FREQ=WEEKLY;UNTIL=20160630T235959Z',
                ],
          'description': ""
        }

      
  
      
    #event = {
    #          'summary': 'Google I/O 2015',
    #            'location': '800 Howard St., San Francisco, CA 94103',
    #           'description': 'A chance to hear more about Google\'s developer products.',
    #            'start': {
    #              'dateTime': '2015-05-28T09:00:00-07:00',
    #              'timeZone': 'America/Los_Angeles',
    #            },
    #            'end': {
    #              'dateTime': '2015-05-28T17:00:00-07:00',
    #              'timeZone': 'America/Los_Angeles',
    #            },
    #            'recurrence': [
    #                 'RRULE:FREQ=WEEKLY;UNTIL=20160630T235959Z',
    #            ],
    #            'attendees': [
    #              {'email': 'lpage@example.com'},
    #              {'email': 'sbrin@example.com'},
    #            ],
    #            'reminders': {
    #              'useDefault': False,
    #              'overrides': [
    #                {'method': 'email', 'minutes': 24 * 60},
    #                {'method': 'popup', 'minutes': 10},
    #              ],
    #            },
    #          }


      event_list.append(add_event)
  return event_list

def clearCalendar(service):

  eventsResult = service.events().list(calendarId=palinsestoId).execute()

  for event in eventsResult['items']:
    service.events().delete(calendarId=palinsestoId, eventId=event['id']).execute()

  return

if __name__ == '__main__':
    main()

