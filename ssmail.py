import smtplib
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import json
import sslib
import os

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def  TurnOffMsg(usrd):
	deadline = usrd['deadline']
	name = usrd['name']
	admin = sslib.GetEtc()['admin']
	txt='Hi ,'+name+'~\n'+'Your Shadowsocks\' Service expire on '+deadline+' and turn off'+'\n'+'Any Problems you can get in touch with admin '+admin+'\n'
	msg = MIMEText(txt, 'plain', 'utf-8')
	return msg

def  ExtendMsg(usrd):
	deadline = usrd['deadline']
	name = usrd['name']
	admin = sslib.GetEtc()['admin']
	txt='Hi ,'+name+'~\n'+'Your Shadowsocks\' Service expire on '+deadline+'\n'+'Any Problems you can get in touch with admin '+admin+'\n'
	msg = MIMEText(txt, 'plain', 'utf-8')
	return msg

def  TurnOnMsg(usrd):
	deadline = usrd['deadline']
	name = usrd['name']
	admin = sslib.GetEtc()['admin']
	txt='Hi ,'+name+'~\n'+'Your Shadowsocks\' Service expire on '+deadline+' and turn on'+'\n'+'Any Problems you can get in touch with admin '+admin+'\n'
	msg = MIMEText(txt, 'plain', 'utf-8')
	return msg


def SendMail(usrd,msg):
	# try:		
	ssetc=sslib.GetEtc()
	from_addr=ssetc['mail_addr']
	passwd=ssetc['mail_passwd']
	to_addr=usrd['mail_addr']
	name = usrd['name']
	admin = sslib.GetEtc()['admin']
	
	smtp = smtplib.SMTP() 
	server=smtplib.SMTP("smtp.sina.com",25)
	# server.set_debuglevel(1)
	server.login(from_addr,passwd)

	msg['From'] = _format_addr(u'%s <%s>' % (admin,from_addr))
	msg['To'] = _format_addr(u'%s <%s>' % (name,to_addr))
	msg['Subject'] = Header(u'Shadowsocks Manager Remind', 'utf-8').encode()

	server.sendmail(from_addr,[to_addr],msg.as_string())
	server.quit()
	sslib.Inhistory('Send mail successfully to '+name)
	# except:
	# 	sslib.Error(2,'Cannot send mail')