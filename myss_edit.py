
import os
import time
import sys
from datetime import datetime,timedelta
import pickle
class ss_user():
	def __init__(self,name,deadline,command):
		self.name=name
		self.deadline=deadline
		self.command=command
	def extend_deadline(self,deadline,month_num):
		self.deadline=max(self.deadline,datetime.now())+timedelta(30*month_num)

def Save(user_list):
	f = open("myss_log",'wb')
	pickle.dump(user_list,f)
	f.close()



def Init():
	user_list= []
	Save(user_list)

def Run():
	leng=len(sys.argv)
	if(leng<=1):
		print "Need Command."
	if(sys.argv[1]=='init'):
		Init()
	# for x in (sys.argv):


def test():	
	user_list= []
	yc = ss_user('yc',datetime.now(),'happy')
	wz = ss_user('wz',datetime.now(),'sad')
	f = open("myss_log",'wb')
	pickle.dump(yc,f)
	f.close()

Run()