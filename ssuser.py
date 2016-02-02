#!/usr/bin/env python
import os
import time
from datetime import datetime,timedelta
import pickle
import commands

def print_date(mytime):
	return str(mytime.year)+'.'+str(mytime.month)+'.'+str(mytime.day)


class ss_user():
	def __init__(self,name,deadline,configpos,mail_addr):
		self.name=name
		self.deadline=deadline
		self.configpos=configpos
		self.mail_addr=mail_addr
		self.pidpos=os.path.join('/tmp','ss_'+name+'.pid')
		self.command='ss-server'+' -c '+self.configpos+' -f '+self.pidpos
	
	def extend_deadline(self,month_num):
		self.deadline=max(self.deadline,datetime.now())+timedelta(30*month_num)

	def print_infomations(self):
		print "Name:"+self.name
		print "Deadline:"+print_date(self.deadline)
		print self.command

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
		(status, output) = commands.getstatusoutput(self.command)

	def offline(self):
		cmd1='kill '+self.getpid()	
		cmd2='rm '+self.pidpos
		(status, output) = commands.getstatusoutput(cmd1)
		(status, output) = commands.getstatusoutput(cmd2)


def Run():
	f = open("myss_log",'rb')
	d= pickle.load(f)
	for x in d:
		print 1
		d.print_infomations()
	f.close()
	
def Sleep():
	time.sleep(3)
# while True:
# 	Run()
# 	Sleep()
# Run()
def test():
	he=ss_user('fa','20150101','~/config_father.json','@')
	#if he.stat() == False :
	#	fa.online()
	he.online()
	he.online()
	print he.getpid()
	print he.stat()
	#he.offline();
	# print type(datetime.now())
# (status, output) = commands.getstatusoutput('sublime ~/tst')
# (status, output) = commands.getstatusoutput('python ~/tst.py')

# print status
# print output 
# print '123'+'32'
test()
