import os

from json import JSONDecoder
from urllib2 import urlopen

import datetime

class updatePalinsesto():
  
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