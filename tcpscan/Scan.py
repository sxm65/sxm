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
    start_time = time.time() # 开始执行的时间
    setdefaulttimeout(1)
    for p in range(1,1024):
        t = threading.Thread(target=portScanner,args=('www.baidu.com',p))#百度
        threads.append(t)
        t.start()     
    end_time = time.time() # 执行的时间
    for t in threads:
        t.join()

    print('[*] The scan is complete!')
    print('[*] A total of %d open port ' % (openNum))
    print("运行了 %3ss"%(end_time-start_time,))
if __name__ == '__main__':
    main()
