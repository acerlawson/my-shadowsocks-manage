#!/usr/bin/env python
import os
import time
from datetime import datetime,timedelta
import pickle
import commands
import json
def date2str(mydate):
	return mydate.strftime("%Y%m%d")

def str2date(mystr):
	return datetime.strptime(mystr,"%Y%m%d")

def MyUsrInit(name,configpos,mail_addr,deadline =date2str(datetime.now())):
	d={}
	d['name']=name
	d['deadline']=deadline
	d['configpos']=configpos
	d['mail_addr']=mail_addr
	d['pidpos']=os.path.join('/tmp','ss_'+name+'.pid')
	d['command']='ss-server'+' -c '+d['configpos']+' -f '+d['pidpos']
	return d
class MyUsr():
	def __init__(self,dd):
		self.dict=dd

	def extend_deadline(self,num):
		self.dict['deadline']=date2str(max(str2date(self.dict['deadline']),datetime.now())+timedelta(num))

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
			(status, output) = commands.getstatusoutput(self.dict['command'])

	def offline(self):
		if self.stat():
			try:			
				cmd1='kill '+self.getpid()	
				cmd2='rm '+self.dict['pidpos']
				(status, output) = commands.getstatusoutput(cmd1)
				(status, output) = commands.getstatusoutput(cmd2)
			except:
				pass



	
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
	#he.offline();
	# print type(datetime.now())
# (status, output) = commands.getstatusoutput('sublime ~/tst') 	
# (status, output) = commands.getstatusoutput('python ~/tst.py')

# print status
# print output 
# print '123'+'32'
#print datetime.now()
#test()
# aaa=123
# print aaa.__name__
# usrlist=[]
# json.dumps(obj)
# encodejson = json.dumps(usrlist,indent=2)
# print encodejson



