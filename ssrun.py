import sslib
import os
import time
from datetime import datetime,timedelta
import pickle
import commands
import json
import ssmail



def TurnOn(usrd):
	ssmail.SendMail(usrd,ssmail.TurnOnMsg(usrd))

def TurnOff(usrd):
	ssmail.SendMail(usrd,ssmail.TurnOffMsg(usrd))



def Check():
	sslib.Inhistory('Routine check')
	usrlist=sslib.GetUsrList()
	nowdate=sslib.nowdate()
	for usrname in usrlist:
		usr = sslib.MyUsr(usrlist[usrname])
		Result = usr.check()
		if Result == 'turnon':
			Inhistory('Turn on '+usrname +'\'s service')
			TurnOn(usrlist[usrname])
		if Result =='turnoff':
			Inhistory('Turn off '+usrname +'\'s service')
			TurnOff(usrlist[usrname])
		
	sslib.Inhistory('End check')


# usrlist=sslib.GetUsrList()
# usr = usrlist['acer']
# TurnOff(usr)
def Start():
	try:
		pidpos=ssetc['pidpos']
	except:
		pidpos='/tmp'
		
	try:		
		pid = os.fork()
		if pid:
			return
		os.chdir(pidpos)
		f=open('ssrun.pid','a')
		print type(os.getpid())
		f.write(str(os.getpid())+'\n')
		f.close()
		os.setsid()
	except:
		sslib.Error(2,'Run Failed')
		return
	sslib.Inhistory('Start Run')
	while 1:
		# Check()
		ssetc=sslib.GetEtc()	
		try:
			sleep=ssetc['sleep']
		except:
			sleep=3600
		time.sleep(sleep)


def Stop():
	try:
		pidpos=ssetc['pidpos']
	except:
		pidpos='/tmp'
	try:	
		os.chdir(pidpos)
		f=open('ssrun.pid','r')
		for i in f.read().split('\n'):
			try:
				if len(i) >0:
					print i
					(status, output) = commands.getstatusoutput('kill '+i)
					print output
			except:
				pass
		f.close()
		os.remove('ssrun.pid')
	except:
		sslib.Error(2,'Cannot Stop')
