from connection import *
from updatePalinsesto import *



def main():

    schedule = {'lu':[],'ma':[],'me':[],'gi':[],'ve':[],'sa':[],'do':[]}

    pal = updatePalinsesto()
    con = connection()

    if pal.updateSchedule(schedule): # qui 
      lis = pal.build_calendar_events(schedule)

      #apro la connessione con google api
      credentials = con.get_credentials()
      http = credentials.authorize(httplib2.Http())
      service = discovery.build('calendar', 'v3', http=http)
      
      
      con.clearCalendar(service)#cancello tutti gli eventi nel calendario
      con.insert_calendar_events(lis, service)#aggiorno il calendario

    else :
      print 'Aggionameto non necessario'




if __name__ == '__main__':
    main()

