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
	txt1='Hi ,'+name+'~\n'
	txt2='Your Shadowsocks\' Service expires on '+deadline+'\n'
	txt3='It was turned off by server\n'
	txt0='\n\n\n\n\n\nDon\'t reply this mail,which was sent by server\'s robot\nAny Problems you can get in touch with admin '+admin+'\n'
	msg = MIMEText(txt1+txt2+txt3+txt0, 'plain', 'utf-8')
	return msg

def  ExtendMsg(usrd):
	deadline = usrd['deadline']
	name = usrd['name']
	admin = sslib.GetEtc()['admin']
	txt1='Hi ,'+name+'~\n'
	txt2='Your Shadowsocks\' Service expires on '+deadline+'\n'
	txt3='Welcome to continue using Shadowsocks\'s service'
	txt0='\n\n\n\n\n\nDon\'t reply this mail,which was sent by server\'s robot\nAny Problems you can get in touch with admin '+admin+'\n'
	msg = MIMEText(txt1+txt2+txt0, 'plain', 'utf-8')
	return msg

def  TurnOnMsg(usrd):
	deadline = usrd['deadline']
	name = usrd['name']
	admin = sslib.GetEtc()['admin']
	txt1='Hi ,'+name+'~\n'
	txt2='Your Shadowsocks\' Service expires on '+deadline+'\n'
	txt3='It was turned on by server\n'
	txt0='\n\n\n\n\n\nDon\'t reply this mail,which was sent by server\'s robot\nAny Problems you can get in touch with admin '+admin+'\n'
	msg = MIMEText(txt1+txt2+txt3+txt0, 'plain', 'utf-8')
	return msg


def SendMail(usrd,msg):

	ssetc=sslib.GetEtc()
	if ssetc['mail'] =='off':
		return
	from_addr=ssetc['mail_addr']
	passwd=ssetc['mail_passwd']
	to_addr=usrd['mail_addr']
	name = usrd['name']

	admin = ssetc['admin']
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
