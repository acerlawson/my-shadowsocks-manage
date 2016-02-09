#!/usr/bin/env python
import sslib
import ssexe
import ssedit
import sys
def Go():	
	if len(sys.argv) > 1:
		if sys.argv[1] == 'init':
			ssedit.UsrListInit()
			return

		if sys.argv[1] == 'start':
			ssexe.Start()
			return

		if sys.argv[1] == 'stop':
			ssexe.Stop()
			return

		if sys.argv[1] == 'check':
			ssexe.Check()
			return

		
		if sys.argv[1] == 'add':
			if len(sys.argv) != 5:
				sslib.Error(1,'Need 4 parameter')
				return
			ssedit.AddUsr(sys.argv[2],sys.argv[3],sys.argv[4])
			return

		if sys.argv[1]=='remove':
			if len(sys.argv) !=3:
				sslib.Error(1,'Need 1 parameter')
				return
			ssedit.RemoveUsr(sys.argv[2])
			return

		if sys.argv[1]=='extend':
			if len(sys.argv)!=4:
				sslib.Error(1,'Need 3 parameter')
				return
			ssedit.Extend(sys.argv[2],int(sys.argv[3]))
			return
	sslib.Error(1,'no command')

Go()