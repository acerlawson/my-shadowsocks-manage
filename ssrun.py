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



def Run():
	sslib.Inhistory('Routine inspection')
	usrlist=sslib.GetUsrList()
	nowdate=sslib.nowdate()
	for usrname in usrlist:
		usr = sslib.MyUsr(usrlist[usrname])
		Result = usr.check()
		if Result == 'turnon':
			Inhistory('Turn on '+usrname)
			TurnOn(usrlist[usrname])
		if Result =='turnoff':
			Inhistory('Turn off '+usrname)
			TurnOff(usrlist[usrname])
		
	sslib.Inhistory('End inspection')


usrlist=sslib.GetUsrList()
usr = usrlist['acer']
TurnOff(usr)

# while 1:
# 	Run()
# 	ssetc=sslib.GetEtc()	
# 	sleep=max(ssetc['sleep'],3600)
# 	time.sleep(sleep)