#!/usr/bin/env python
import os
import time
from datetime import datetime,timedelta
import pickle
import commands
import json


def GetEtc():
	f=open('/home/acerlawson/ssetc.json','rb')
	ssetc=json.loads(f.read())
	f.close()
	return ssetc

def GetUsrList():
	f=open("usrlist.json",'rb')
	usrlist=json.loads(f.read())
	f.close()
	return usrlist

def SaveUsrList(usrlist):
	f=open("usrlist.json",'wb')
	f.write(json.dumps(usrlist,indent=2))
	f.close()
	return True

def Judge(question):
	question=question+" ......y/n?"
	respon = raw_input(question)
	if respon[0]=='y' or respon[0]=='Y':
		return True
	return False
def Inhistory(info):
	f=open('history','a')
	print info
	f.write(datetime.now().strftime("%F %H:%M:%S")+'	'+info+'\n')
	f.close()


def Success(Suinfo):
	info='Successfully '+Suinfo
	Inhistory(info)
def Error(Errnum,Errinfo):
	if Errnum == 0:
		Errtype='Logic'
	elif Errnum ==1:
		Errtype='Input'
	else:
		Errtype='Unknown'

	info='Error '+Errtype+'('+str(Errnum)+')'+':   '+Errinfo
	Inhistory(info)


def date2str(mydate):
	return mydate.strftime("%Y-%m-%d")
def str2date(mystr):
	return datetime.strptime(mystr,'%Y-%m-%d')
def nowdate():
	return date2str(datetime.now())

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
		# print num
		print '------------------------'
		print str2date(self.dict['deadline'])
		self.dict['deadline']=date2str(str2date(max(self.dict['deadline'],nowdate))+timedelta(num))

	def getpid(self):
		try:
			f=open(self.pidpos,'r')
			num=f.read()
			f.close()
			return str(int(num))
		except:
			return None
	def stat(self):
		#0 -> offline ,1 -> online
		mypid=self.getpid()
		if mypid :
			cmd='ps '+mypid;
			(status, output) = commands.getstatusoutput(cmd)
			if output.find(mypid) >= 0:
				return True
		return False

	def online(self):
		if not self.stat():
			try:
				(status, output) = commands.getstatusoutput(self.dict['command'])
			except:
				pass

	def offline(self):
		if self.stat():
			try:			
				cmd1='kill '+self.getpid()	
				cmd2='rm '+self.dict['pidpos']
				(status, output) = commands.getstatusoutput(cmd1)
				(status, output) = commands.getstatusoutput(cmd2)
			except:
				pass

	def check(self):
		oldstat=self.stat()
		
		if self.dict['deadline']<=nowdate:
			self.offline()
		else:
			self.online()
		newstat=self.stat()

		if oldstat == newstat :
			return 'keep'

		elif oldstat == False and newstat ==True:	
			return 'turnon'

		elif oldstat == True and  oldstat == False:
			return 'turnoff'
	def  usrprint(self):
		usrjson=json.dumps(self.dict,indent = 4)
		print usrjson




	
def Sleep():
	time.sleep(3)

def test():
	he=MyUsr(MyUsrInit(name = 'fa',configpos = '~/config_father.json', mail_addr ='@'))
	#if he.stat() == False :
	#	fa.online()
	he.online()
	print he.getpid()
	print he.dict
	he.extend_deadline(3)
	print he.dict


