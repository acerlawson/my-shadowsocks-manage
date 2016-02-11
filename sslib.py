#!/usr/bin/env python

__author__='acerlawson'
__email__='acerlawson@gmail.com'
###################################################
#important
#This one is differ from man to man
#It's the dir which storage 'ssetc.json' and 'usrlist.json' and 'history'
#'ssetc.json' is necessary before running all the process
#how to wirte the 'ssetc.json',you can read 'readme.txt'
global ssdir
ssdir='/home/acerlawson'
###################################################
###################################################
###################################################

import os
import time
from datetime import datetime,timedelta
import commands
import json
import ssedit



def GetEtc():
	#Read and Return ssetc
	os.chdir(ssdir)
	#if no such file, gg simida
	if not os.path.exists("ssetc.json"):
		return None
	f=open("ssetc.json",'rb')
	ssetc=json.loads(f.read())
	f.close()
	return ssetc

def GetUsrList():
	#Read and Return usrlist
	os.chdir(ssdir)

	#if no such file, create one
	if not os.path.exists("usrlist.json"):
		usrlist={}
		SaveUsrList(usrlist)

	f=open("usrlist.json","rb")
	usrlist=json.loads(f.read())
	f.close()
	# print usrlist
	return usrlist

def SaveUsrList(usrlist):
	#Write usrlist in 'usrlist.json'
	os.chdir(ssdir)
	f=open("usrlist.json","wb")
	f.write(json.dumps(usrlist,indent=2))
	f.close()
	return True

def Judge(question):
	#Read the string from the keyboard and Judge yes or no ,y/n?
	question=question+" ......y/n?"
	respon = raw_input(question)
	if respon[0]=='y' or respon[0]=='Y':
		return True
	return False
def Inhistory(info):
	#It's to record everything and the time
	os.chdir(ssdir)
	f=open('history','a')
	print info
	f.write(datetime.now().strftime("%F %H:%M:%S")+'	'+info+'\n')
	f.close()


def Success(Suinfo):
	# Successful operation
	info='Successfully '+Suinfo
	Inhistory(info)

def Error(Errnum,Errinfo):
	# Not good operation
	if Errnum == 0:
		Errtype='Logic'
	elif Errnum ==1:
		Errtype='Input'
	else:
		Errtype='Unknown'

	info='Error '+Errtype+'('+str(Errnum)+')'+':   '+Errinfo
	Inhistory(info)

#change date and string in my own way
def date2str(mydate):
	return mydate.strftime("%Y-%m-%d")
def str2date(mystr):
	return datetime.strptime(mystr,'%Y-%m-%d')

#return the now time as string in my own way
def nowdate():
	return date2str(datetime.now())

#Change the 'dict' to the 'MyUsr'
def MyUsrInit(name,configpos,mail_addr,deadline =nowdate()):
	d={}
	d['name']=name
	d['deadline']=deadline
	d['configpos']=configpos
	d['mail_addr']=mail_addr

	piddir='/tmp'
	try:
		ssetc=GetEtc()
		piddir=ssetc['piddir']
	except:
		Error(2,'No piddir in json')
	d['pidpos']=os.path.join(piddir,'ss_'+name+'.pid')
	
	d['command']='ss-server'+' -c '+d['configpos']+' -f '+d['pidpos']
	
	return d

class MyUsr():
	def __init__(self,dd):
		self.dict=dd

	def extend(self,num):
		#extend deadline
		self.dict['deadline']=date2str(str2date(max(self.dict['deadline'],nowdate()))+timedelta(num))

	def getpid(self):
		#get pid pos and return
		pidpos =self.dict['pidpos']
		if os.path.exists(pidpos):
			f=open(pidpos,'r')
			num=f.read()
			f.close()
			return str(int(num))
		else:
			return None
	def stat(self):
		#Judge wheter the process online
		#False -> offline ,True-> online
		mypid=self.getpid()
		if mypid :
			cmd='ps '+mypid
			(status, output) = commands.getstatusoutput(cmd)
		#	print output
			if output.find(mypid) >= 0:
				return True
		return False

	def online(self):
		#turn on
		if not self.stat():
			(status, output) = commands.getstatusoutput(self.dict['command'])
			if status == 0:
				return True
		return False

	def offline(self):
		#turn off
		if self.stat():	
			cmd1='kill '+self.getpid()	
			cmd2='rm '+self.dict['pidpos']
			(status1, output1) = commands.getstatusoutput(cmd1)
			(status2, output2) = commands.getstatusoutput(cmd2)
			if not self.stat():
				return True
		return False

	def check(self):
		#check whether turn on or turn off
		oldstat=self.stat()
		if self.dict['deadline']<=nowdate():
			if self.offline():
				return 'turnoff'
		else:
			if self.online():
				return 'turnon'
		return 'keep'


	def  view(self):
		#return simple information
		name =self.dict['name']
		deadline=self.dict['deadline']
		stat='Online' if self.stat() else 'Offline'
		print '%18s|%s|%s '%(name,deadline,stat)

	def jsoninfo(self):
		#return all information
		return json.dumps(self.dict,indent=2)



