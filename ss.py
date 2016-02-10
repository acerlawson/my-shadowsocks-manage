#!/usr/bin/env python
import sslib
import ssexe
import ssedit
import sys

__author__='acerlawson'
__email__='acerlawson@gmail.com'

def Go():	
	if len(sys.argv) > 1:
		#----------------------------------------------------exe-----------------------------------------
		#start the ssmanage service,which will check automatically
		if sys.argv[1] == 'start':
			ssexe.Start()
			return

		#stop the ssmanage service and turn off all shadowsocks service process
		if sys.argv[1] == 'stop':
			ssexe.Stop()
			return

		#view the ssmanage service and all shadowsocks service process status
		if sys.argv[1] == 'view':
			ssexe.View()
			return

		#manually check the shadowsocks service 
		if sys.argv[1] == 'check':
			ssexe.Check()
			return
		#---------------------------------------------------edit------------------------------------------	
		#initalize the usrlist.json
		if sys.argv[1] == 'init':
			ssedit.UsrListInit()
			return
		
		#add new user in usrlist.json
		#command: add usrname cofigposition email_address
		if sys.argv[1] == 'add':
			if len(sys.argv) != 5:
				sslib.Error(1,'Need 4 parameter')
				return
			ssedit.AddUsr(sys.argv[2],sys.argv[3],sys.argv[4])
			return

		#remove user in usrlist.json
		#command: remove usrname 
		if sys.argv[1]=='remove':
			if len(sys.argv) !=3:
				sslib.Error(1,'Need 1 parameter')
				return
			ssedit.RemoveUsr(sys.argv[2])
			return
			
		#remove user in usrlist.json
		#command: extend usrname days
		if sys.argv[1]=='extend':
			if len(sys.argv)!=4:
				sslib.Error(1,'Need 3 parameter')
				return
			ssedit.Extend(sys.argv[2],int(sys.argv[3]))
			return
	sslib.Error(1,'no command')

Go()