#!/usr/bin/env python
import os
import time
from datetime import datetime,timedelta
import commands
import json
import sys
import sslib,ssmail
import copy

def UsrListInit():
	#Write init command in history
	sslib.Inhistory('Command: '+'init')
	usrlist={}
	sslib.SaveUsrList(usrlist)
	sslib.Success('init')

def Extend(name,days):
	#Write extend command in history
	sslib.Inhistory('Command: '+'extend   name = '+name+',  days = '+str(days))
	
	#Get usrlist
	usrlist=sslib.GetUsrList()
	if name in usrlist:
		#First,we get each users' information
		oldusr=sslib.MyUsr(usrlist[name])
		
		#Second,we copy the informaiton
		newusr=sslib.MyUsr(copy.deepcopy(oldusr.dict))
		
		#Third,we extend the deadline on the copy
		newusr.extend(days)
		
		#query y/n?
		if sslib.Judge(oldusr.dict['deadline']+'	----->	'+newusr.dict['deadline']):
			#if yes
			usrlist[name]=newusr.dict
			
			#change the usrlist by newusr
			if not sslib.SaveUsrList(usrlist):
				sslib.Error(2,'cannot save')
				return 
			sslib.Success('extend '+name+' to '+usrlist[name]['deadline'])
			
			#And write email to the usr
			ssmail.SendMail(usrlist[name],ssmail.ExtendMsg(usrlist[name]))

		else:
			sslib.Error(0,'Cancel')
			return
	else:
		sslib.Error(0,'No such name')
		return


def AddUsr(name,configpos,mail_addr):
	#Write add command in history
	sslib.Inhistory('Command: '+'add   name= '+name+',  configpos= '+configpos+',  mail_addr= '+mail_addr)
	
	#Get usrlist
	usrlist=sslib.GetUsrList()
	#Initialize usr
	usr=sslib.MyUsr(sslib.MyUsrInit(name,configpos,mail_addr))
	
	#check whether usr in usrlist
	if name in usrlist:
		sslib.Error(0,'Name already exists')
		return
 	
 	#print the information to the 
	print usr.jsoninfo()

	#Ask whether add the usr
	if sslib.Judge('Confirm add'):
		usrlist[name]=usr.dict
		sslib.SaveUsrList(usrlist)
		sslib.Success('add')
	else:
		sslib.Error(0,'Cancel')


def RemoveUsr(name):
	#Write remove command in history
	sslib.Inhistory('Command: '+'remove    name= ',name)
	usrlist=sslib.GetUsrList()
	if name in usrlist:
		#Ask whether remove
		if sslib.Judge('Remove '+name):
			usrlist.pop(name)
			sslib.SaveUsrList(usrlist)
			sslib.Success('remove')

		else:
			sslib.Error(0,'Cancel')

	else:
		sslib.Error(0,'No such name')
