#!/usr/bin/env python
import os
import time
from datetime import datetime,timedelta
import pickle
import commands
import json
import sys
import ssuser

def UsrListInit():
	usrlist={}
	SaveUsrList(usrlist)


def SaveUsrList(usrlist):
	f=open("usrlist.json",'wb')
	f.write(json.dumps(usrlist,indent=2))
	f.close()

def GetUsrList():
	f=open("usrlist.json",'rb')
	usrlist=json.loads(f.read())
	f.close()
	return usrlist

def AddUsr(name,configpos,mail_addr):
	usrlist=GetUsrList()
	dd=ssuser.MyUsrInit(name,configpos,mail_addr)
	#yao pan duan 'name' shi fou bei yong guo
	usrlist[name]=dd
	SaveUsrList(usrlist)



def Go():	
	if len(sys.argv) > 0:
		if sys.argv[1] == 'init':
			UsrListInit()


UsrListInit()
AddUsr(name = 'fa',configpos = '~/config_father.json', mail_addr ='@')
print GetUsrList()