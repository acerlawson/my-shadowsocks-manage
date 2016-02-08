#!/usr/bin/env python
import os
import time
from datetime import datetime,timedelta
import pickle
import commands
import json
import sys
import sslib,ssmail
import copy

def UsrListInit():
	sslib.Inhistory('Command: '+'init')
	usrlist={}
	sslib.SaveUsrList(usrlist)
	sslib.Success('init')

def Extend(name,days):
	sslib.Inhistory('Command: '+'extend   name = '+name+',  days = '+str(days))
	usrlist=sslib.GetUsrList()
	try:	
		if name in usrlist:
			oldusr=sslib.MyUsr(usrlist[name])
			newusr=sslib.MyUsr(copy.deepcopy(oldusr.dict))
			newusr.extend(days)
			if sslib.Judge(oldusr.dict['deadline']+'	----->	'+newusr.dict['deadline']):
				usrlist[name]=newusr.dict
				if not sslib.SaveUsrList(usrlist):
					sslib.Error(2,'cannot save')
					return 
				sslib.Success('extend '+name+' to '+usrlist[name]['deadline'])
				ssmail.SendMail(usrlist[name],ssmail.ExtendMsg(usrlist[name]))

			else:
				sslib.Error(0,'Cancel')
				return
		else:
			sslib.Error(0,'Name already exists')
			return
	except:
		sslib.Error(2,'Something wrong')


def AddUsr(name,configpos,mail_addr):
	sslib.Inhistory('Command: '+'add   name= '+name+',  configpos= '+configpos+',  mail_addr= '+mail_addr)
	usrlist=sslib.GetUsrList()
	usr=sslib.MyUsr(sslib.MyUsrInit(name,configpos,mail_addr))
	#print usrlist
	if name in usrlist:
		sslib.Error(0,'Name already exists')
		return

	# cha kan config shi fou cun zai 
	usr.usrprint()
	if sslib.Judge('Confirm add'):
		usrlist[name]=usr.dict
		sslib.SaveUsrList(usrlist)
		sslib.Success('add')
	else:
		sslib.Error(0,'Cancel')


def RemoveUsr(name):
	sslib.Inhistory('Command: '+'remove    name= ',name)
	usrlist=sslib.GetUsrList()
	if name in usrlist:
		if sslib.Judge('Remove '+name):
			usrlist.pop(name)
			sslib.SaveUsrList(usrlist)
			sslib.Success('remove')

		else:
			sslib.Error(0,'Cancel')

	else:
		sslib.Error(0,'No such name')


def Go():	
	if len(sys.argv) > 1:
		if sys.argv[1] == 'init':
			UsrListInit()
			return
		
		if sys.argv[1] == 'add':
			if len(sys.argv) != 5:
				sslib.Error(1,'Need 4 parameter')
				return
			AddUsr(sys.argv[2],sys.argv[3],sys.argv[4])
			return

		if sys.argv[1]=='remove':
			if len(sys.argv) !=3:
				sslib.Error(1,'Need 1 parameter')
				return
			RemoveUsr(sys.argv[2])
			return

		if sys.argv[1]=='extend':
			if len(sys.argv)!=4:
				sslib.Error(1,'Need 3 parameter')
				return
			Extend(sys.argv[2],int(sys.argv[3]))
			return
	sslib.Error(1,'no command')






Go()
#sslib.Inhistory('123')
# UsrListInit()
# AddUsr(name = 'lihongji',configpos = '~/config.json', mail_addr ='acerlawson@gmail.com')
# print GetUsrList()
# for usr in GetUsrList():
# 	usr.usrprint()
# RemoveUsr('dfa')
# print GetUsrList()
# extend_deadline('dfa',3)
# a=input()
# print a