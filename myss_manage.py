
import os
import time
from datetime import datetime,timedelta
import pickle
class ss_user():
	def __init__(self,name,deadline,command):
		self.name=name
		self.deadline=deadline
		self.command=command
	def extend_deadline(self,deadline,month_num):
		self.deadline=max(self.deadline,datetime.now())+timedelta(30*month_num)


def Run():
	f = open("myss_log",'rb')
	d= pickle.load(f)
	print d.deadline
	f.close()
	
def Sleep():
	time.sleep(3)
while True:
	Run()
	Sleep()
