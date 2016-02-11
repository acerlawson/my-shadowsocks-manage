

**ss-manage**
-------------

 - 简介:

    **ss-manage**是在**shadowosocks-libev** 基础上，在服务器上简单管理多个**ss-server**进程的一个项目。通过启动一个后台管理进程，根据预设的参数（如**时间**等），自动打开或关闭ss-server的进程，同时附带 邮件提醒 等操作

 - 环境:
    
    os：centos 6.7/ubuntu 14.04
    
    编译环境：python 2.6/2.7

 - 须知:

    软件由4个文档文件readme.txt、ssetc.json、usrlist.json、history
    
    和5个程序文件ss.py、ssedit.py、ssexe.py、ssmail.py、sslib.py组成
    
    首先**必须在sslib.py中设置ssdir路径变量**（默认是自己的用户的主文件夹）
    
    ssdir是用于存放ssetc.json、usrlist.json、history的目录
    
    其中ssetc.json十分重要，使用者手动设置
    
    
    	{
    		"sleep":7200,#表示后台管理进程每次检查的间隔，这里是7200s=2h
    		"piddir":"/tmp",#表示存放pid的位置
    		"mail_addr":"example@xxx.com",#表示管理员的邮箱
    		"mail_passwd":"mailpasswd",#表示邮箱对应密码	
    		"smtp_server":"smtp.xxx.com",#对应邮箱的smtp服务器地址
    		"admin":"Hongji Li",#管理员姓名，发送提醒邮件的时候会用到
    		"mail":"on"#是否打开邮件功能
    	}
	

 - 命令

>**./ss.py command**


        针对后台管理进程的命令
        
        start 
        #启动后台程序ssmanage，该后台程序会隔一段时间自动调用check
        
        stop 
        #停止后台程序ssmanage 并且 关闭所有shadowsocks服务
        
        view 
        #查看后台程序的运行时间和shadowsocks服务的状态
        
        check 
        #手动启动check、一般是修改了usrlist后可以快速地响应修改
        
        
        
        
        针对usrlist的命令
        
        init 
        #初始化usrlist
        
        add usrname config_position email_address 
        #添加新的用户
        
        remove usrname 
        #删除用户
        
        extend usrname days 
        #延长用户使用时间


----------------嫌麻烦的话，上面全部设置完以后，以下的可以直接跳过直接开始使用--------



 - usrlist.json

    是存放每个ss-server进程用户的基本信息，程序自动创建，可以直接使用
    
    
 - history

    是记录每个管理员或程序的操作和发生的时间



 - sslib.py 包括了需要基本的类（如端口）和一些中间函数（如格式转化）
	
        class MyUsr()
        	属性设计考虑再三，最后打算简单地用dict实现
        	包括了初始化，上线，下线，输出等函数
        
        def Judge()用于和管理员交互的函数(y/n?)
        def Sucess()用于错误输出
        def Error()用于错误输出
        def GetEtc()用于获取ssetc文件内容
        def GetUsrList()用于获取usrlist文件内容
        def Inhistory()将过程写入history中
        def str2date()\date2str() 日期和字符串相互转换
        def nowdate()返回服务器当前时间


		
 - ssedit.py包括对用户信息的更新，包括添删用户、延长时间等，被操作的具体文件是 usrlist.json
	
        def UsrListInit() 初始化usrlist
        def Extend(name,days) 延长时间
        def AddUsr(name,configpos,mail_addr)添加用户
        def RemoveUsr(name)删除用户

 - ssexe.py 包括ssmanage的主要运行部分，包括start、stop、check、view等


 - ssmail.py 包括发送邮件提醒给用户，通过给用户发送提醒信息，包括邮件类型包括（启动/关闭/延长shadowsocks），可以自己修改代码DIY





__author__=acerlawson


__mail__=acerlawson@gmail.com


