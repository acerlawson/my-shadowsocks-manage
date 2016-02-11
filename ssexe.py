#!/usr/bin/env python

__author__='acerlawson'
__email__='acerlawson@gmail.com'

import sslib
import os
import time
from datetime import datetime,timedelta
import commands
import json
import ssmail


def TurnOn(usrd):
	#send TurnOnMsg mail to the usrd
	ssmail.SendMail(usrd,ssmail.TurnOnMsg(usrd))

def TurnOff(usrd):
	#send TurnOffMsg mail to the usrd
	ssmail.SendMail(usrd,ssmail.TurnOffMsg(usrd))



def Check():
	#Write check command in history
	sslib.Inhistory('Routine check')

	#Read the usrlist
	usrlist=sslib.GetUsrList()
	
	#Get now time to check
	nowdate=sslib.nowdate()
	for usrname in usrlist:
		#change 'dict' to 'MyUsr'
		usr = sslib.MyUsr(usrlist[usrname])
		#Check the usr
		Result = usr.check()
		print Result
		if Result == 'turnon':
			#Write the result in history
			sslib.Inhistory('Turn on '+usrname +'\'s service')
			TurnOn(usrlist[usrname])
		if Result =='turnoff':
			#Write the result in history
			sslib.Inhistory('Turn off '+usrname +'\'s service')
			TurnOff(usrlist[usrname])
	#Write check command in history		
	sslib.Inhistory('End check')





def Start():
	#Write start command in history
	sslib.Inhistory('Command: '+'Start')
	#try to get the piddir 
	try:
		ssetc=sslib.GetEtc()
		piddir=ssetc['piddir']
	except:
		piddir='/tmp'
	#Through piddir get the pidpos
	pidpos=os.path.join(piddir,'ssrun.pid')	

	#Prepare for running in the background
	pid = os.fork()
	if pid:
		return
	os.setsid()

	#Write the pid in the ssrun.pid
	f=open(pidpos,'a')
		# print type(os.getpid())
	f.write(str(os.getpid())+'\n')
	f.close()

	#Write in history
	sslib.Inhistory('Start Run')
	while 1:
		Check()
		ssetc=sslib.GetEtc()	
		try:
			sleep=ssetc['sleep']
		except:
			sleep=3600
		time.sleep(sleep)


def Stop():
	#Write stop command in history
	sslib.Inhistory('Command: '+'Stop')
	
	#First, turn off all shadowsocks service process 
	usrlist=sslib.GetUsrList()
	nowdate=sslib.nowdate()
	for usrname in usrlist:
		usr = sslib.MyUsr(usrlist[usrname])
		if usr.offline():
			sslib.Inhistory('Turn off '+usrname +'\'s service')
			TurnOff(usrlist[usrname])
	sslib.Success('Kill all service')	

	#Second, turn off the Start() service process

	#To get pidpos
	try:
		ssetc=sslib.GetEtc()
		piddir=ssetc['piddir']
	except:
		piddir='/tmp'
	pidpos=os.path.join(piddir,'ssrun.pid')

	if os.path.exists(pidpos):
		f=open(pidpos,'r')
		txt=f.read().split('\n')
		f.close()
		for i in txt:
			if len(i) >0:
				# print i
				(status, output) = commands.getstatusoutput('kill '+i)
				if status ==0:
					sslib.Inhistory('Kill '+i)
				# print output
		#After kill the process,remember to remove 'ssrun.pid'
		os.remove(pidpos)

		sslib.Success('Stop')
	else:
		#No such file
		sslib.Error(2,'No such file')


def View():
	#Try to get pidpos
	try:
		ssetc=sslib.GetEtc()
		piddir=ssetc['piddir']
	except:
		piddir='/tmp'
	pidpos=os.path.join(piddir,'ssrun.pid')
	
	#In order to show the pid of ssrun and how much the time it has ran
	if os.path.exists(pidpos):
		f=open(pidpos,'r')
		txt=f.read().split('\n')
		f.close()
		for i in txt:
			if len(i) >0:
				# print i
				(status, output) = commands.getstatusoutput('ps -eo pid,etime |grep '+i)
				print output

	#In order to show each usr shadowsocks service process running status
	usrlist=sslib.GetUsrList()
	for usrname in usrlist:
		usr = sslib.MyUsr(usrlist[usrname])
		usr.view()
