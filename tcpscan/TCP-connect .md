#TCP-connect扫描
##1.端口扫描原理：
端口扫描，顾名思义，就是逐个对一段端口或指定的端口进行扫描。通过扫描结果可以知道一台计算机上都提供了哪些服务，然后就可以通过所提供的这些服务的己知漏洞就可进行攻击。其原理是当一个主机向远端一个服务器的某一个端口提出建立一个连接的请求，如果对方有此项服务，就会应答，如果对方未安装此项服务时，即使你向相应的端口发出请求，对方仍无应答，利用这个原理，如果对所有熟知端口或自己选定的某个范围内的熟知端口分别建立连接，并记录下远端服务器所给予的应答，通过查看一记录就可以知道目标服务器上都安装了哪些服务，这就是端口扫描，通过端口扫描，就可以搜集到很多关于目标主机的各种很有参考价值的信息。例如，对方是否提供FPT服务、WWW服务或其它服务。
##2.tcp-connect扫描：
TCP connect() 扫描  这是最基本的TCP扫描。操作系统提供的connect（）系统调用，用来与每一个感兴趣的目标计算机的端口进行连接。如果端口处于侦听状态，那么connect（）就能成功。否则，这个端口是不能用的，即没有提供服务。这个技术的一个最大的优点是，你不需要任何权限。系统中的任何用户都有权利使用这个调用。另一个好处就是速度。如果对每个目标端口以线性的方式，使用单独的connect（）调用，那么将会花费相当长的时间，你可以通过同时打开多个套接字，从而加速扫描。使用非阻塞I/O允许你设置一个低的时间用尽周期，同时观察多个套接字。但这种方法的缺点是很容易被发觉，并且被过滤掉。目标计算机的logs文件会显示一连串的连接和连接是出错的服务消息，并且能很快的使它关闭。
###tcp-connect扫描原理：
TCP connect()扫描原理是：扫描主机通过TCP/IP协议的三次握手与目标主机的指定端口建立一次完整的连接。连接由系统调用connect开始。如果端口开放，则连接将建立成功；否则，若返回-1则表示端口关闭。

##3.**实验要求**：
设计一个程序做到：
（1）输入目的IP地址以及端口范围；         
（2）设置获取的用户输入IP地址为远程IP地址；         
（3）从开始端口到结束端口依次扫描，每扫描一个端口创建一个新的套接字；         
（4）设置远程地址信息中的端口号为需要扫描的当前端口号；         （5）连接到当前端口号的目的地址；         
（6）若连接成功（ connect（）函数返回0 ）则输出该端口为开启状态，否则输出该端口为关闭状态；         
（7）关闭当前套接字。 进阶1，采用半连接提高扫描效率。 进阶2，使用多进程进行端口扫描，进一步提高效率。
##4.实验代码：
	#!/usr/bin/python3
	# -*- coding: utf-8 -*-
	from socket import *
	import threading
	import time, sys

	lock = threading.Lock()
	openNum = 0
	threads = []

	def portScanner(host,port):
    	global openNum
    	try:
        	s = socket(AF_INET,SOCK_STREAM)
        	s.connect((host,port))
        	lock.acquire()
        	openNum+=1
        	print('[+] %d open' % port)
        	lock.release()
        	s.close()
    	except:
        	pass

	def main():
    	start_time = time.time() # 脚本开始执行的时间
    	setdefaulttimeout(1)
    	for p in range(1,1024):
        	t = threading.Thread(target=portScanner,args=('www.baidu.com',p))#百度
       	 	threads.append(t)
        	t.start()     
   	 	end_time = time.time() # 结束执行的时间
    	for t in threads:
        	t.join()

    	print('[*] The scan is complete!')
    	print('[*] A total of %d open port ' % (openNum))
    	print("运行了 %3ss"%(end_time-start_time,))
	if __name__ == '__main__':
    	main()
##5.实验结果
##对百度和手机进行了扫描实验结果如下
###1.www.baidu.com
     
        [+] 80 open
	[+] 443 open
	[*] The scan is complete!
	[*] A total of 2 open port 
	运行了 0.9594316482543945s







###2.对安卓手机的端口扫描结果
         [*] The scan is complete!
	 [*] A total of 0 open port 
	 运行了 0.9384949207305908s


##6.结果分析与总结

扫描到百度开放的端口：

    443端口：基于 TLS/SSL 的网页浏览端口，能提供加密和通过安全端口传输的另一种 HTTP

    843端口：flash发起socket通信请求的时候会先寻找服务器端的843端口


安卓手机扫描时端口开放数为0，扫描不到出端口的情况。
这是因为手机在进行网络数据传输的时候，会开启端口，一旦数据发送或者接受完成，端口就自动关闭。在这个时间段内，不会收到响应包。
所以刚开始我扫描了好几次，一直是扫描不到端口，于是上网查找资料才明白。
另外我对百度进行了端口扫描，发现扫描到两个端口443和843.
