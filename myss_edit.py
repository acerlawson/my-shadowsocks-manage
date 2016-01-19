
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
yc = ss_user('yc',datetime.now(),'happy')
f = open("myss_log",'wb')
pickle.dump(yc,f)
f.close()
