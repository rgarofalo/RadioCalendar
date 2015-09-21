
from connection import *
from updatePalinsesto import *



def main():

    schedule = {'lu':[],'ma':[],'me':[],'gi':[],'ve':[],'sa':[],'do':[]}

    pal = updatePalinsesto()

    if pal.updateSchedule(schedule):
      lis = pal.build_calendar_events(schedule)

      
      credentials = connection.get_credentials()
      http = credentials.authorize(httplib2.Http())
      service = discovery.build('calendar', 'v3', http=http)
      
      
      connection.clearCalendar(service)#cancello tutti gli eventi nel calendario
      connection.insert_calendar_events(lis, service)

    else :
      print 'Aggionameto non necessario'




if __name__ == '__main__':
    main()

