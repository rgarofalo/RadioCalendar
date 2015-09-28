from connection import *
from updatePalinsesto import *
from updateOnAir import *

import os


def main():

  palinsestoId ='xxxx@group.calendar.google.com'
  OnAirId='xxxxx@group.calendar.google.com'
  pathReg= "xxxxx"

  pal = updatePalinsesto()

  if pal.updateSchedule(): 
    lis = pal.build_calendar_events()

    #apro la connessione con google api
    con = connection()
    con.IdCalendar=palinsestoId

    credentials = con.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    
   
    
    con.clearCalendar(service,palinsestoId)#cancello tutti gli eventi nel calendario
    con.insert_calendar_events(lis, service)#aggiorno il calendario
    
    print'Palinsesto: Aggionameto'

  else :
    print 'Palinsesto: Aggionameto non necessario'


  
  onair= updateOnAir()

  onair.path= pathReg
  onair.readFilename()
  onair.build_calendar_events()
  
  if len(onair.event_list)>0:

    #apro la connessione con google api
    con = connection()
    con.IdCalendar=OnAirId

    credentials = con.get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http) 

    #con.clearCalendar(service)#cancello tutti gli eventi nel calendario
    con.insert_calendar_events(onair.event_list, service)#aggiorno il calendario
    print'Calendario OnAir aggiornato'

  else :
    print'Calendario OnAir non aggiornato'



    

   


if __name__ == '__main__':
    main()

