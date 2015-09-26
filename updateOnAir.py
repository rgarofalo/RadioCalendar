import os
from datetime import datetime, timedelta

class updateOnAir():
	
	def __init__(self):
		self.list_onair = []
		self.event_list = []
		self.path=""

	def readFilename(self):	
		
		if self.path=="":
			print "inserire path per leggere i file"
		else:
			for file in os.listdir(self.path):
				if file.endswith(".cue"):
					data=datetime.strptime(file,'idjc.[%Y-%m-%d][%H_%M_%S].01.cue')
					self.list_onair.append(data)

	def build_calendar_events(self): 
		for onair in self.list_onair:
			add_event = {
				'summary': 'onair',
				'location': 'pisa',
				'start': {
					'dateTime': str(onair.strftime("%Y-%m-%d")) + "T" +str((onair-timedelta(hours=1)).strftime("%H:%M:%S")) +"+01:00",
					'timeZone': "Europe/Rome"
				},
				'end': {
					'dateTime': str(onair.strftime("%Y-%m-%d")) + "T" + str((onair+timedelta(minutes=15)).strftime("%H:%M:%S")) +"+01:00",
					'timeZone': "Europe/Rome"
				},
				'description': ""
			}

			self.event_list.append(add_event)

  
