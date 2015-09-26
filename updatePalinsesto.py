import os

from json import JSONDecoder
from urllib2 import urlopen

import datetime

class updatePalinsesto():

  def __init__(self):
      self.schedule = {'lu':[],'ma':[],'me':[],'gi':[],'ve':[],'sa':[],'do':[]}

  
  def updateSchedule(self): # This function will update the schedule
        
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
          minList=self.minimalList(listaProgs);
          for today in days:
             self.schedule[today] = filter(lambda t:t['title']!='Musica No Stop',filter(lambda x: x['start'][0] == today, minList))
        
        return True

  def minimalList(self,listaProgs):

    minList = []
    for prog in listaProgs:
      dictionary={'title':prog['title'],'start':prog['start'],'end':prog['end']}
      minList.append(dictionary)

    return minList


  def build_calendar_events(self): 
    event_list = []
    weekdays = ['lu','ma','me','gi','ve','sa','do']

    now = datetime.datetime.today()
    today = now.day
    weekday=now.weekday()

    for day in weekdays:
      for prog in self.schedule[day]:

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


        event_list.append(add_event)
    return event_list