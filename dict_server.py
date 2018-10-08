'''
name:Tedu
data:2018-10-1
email:
modules:
电子辞典开发流程
１．根据需求设计框架
２．指定工作流程
３．完成技术总结和设计
４．完成数据库设计
５．搭建通信框架
６．完成具体功能设计
７．编码实现
'''

from socket import *
import os
import time
import signal
import pymysql
import sys

#定义需要的全局变量
DICI_TEXT = './dict.txt'
HOST = '0.0.0.0'
PORT = 8888
ADDR = (HOST,PORT)

#流程控制
def main():
    #创建数据库连接
    db = pymysql.connect('localhost','root','123456','dict')
    #创建套接字
    s = socket()
    s.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    s.bind(ADDR)
    s.listen(5)

    #忽略子进程信号
    signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            c,addr = s.accept()
            print('Connect from',addr)
        except KeyboardInterrupt:
            s.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue

        #创建子进程

        pid = os.fork()
        if pid == 0:
            s.close()
            print('子进程准备处理请求')
            do_child(c,db)
        else:
            c.close()
            continue


def do_child(c,db):
    while True:
        print(111)
        data = c.recv(128).decode()
        print(data)
        print("Request:",data)
        if (not data) or data[0] == 'E':
            c.close()
            sys.exit()
        elif data[0] == 'R':
            do_register(c,db,data)
        elif data[0] == 'L':
            do_login(c,db,data)
            print(111)
        elif data[0] == 'Q':
            do_query(c,db,data)
        elif data[0] == 'H':
            do_hist(c,db,data)
def do_login(c,db,data):
    l = data.split(' ')
    name = l[1]
    pwd = l[2]

    cursor = db.cursor()
    sql = "select * from user where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchone()

    if r != None:
        p = list(r)
        if r[2] == pwd:
            c.send('OK'.encode())
            print('%s登录成功'%name)
        else:
            c.send('pwd error'.encode())
    else:
        c.send('None'.encode())
    
        
def do_register(c,db,data):
    l = data.split(' ')
    name = l[1]
    pwd = l[2]

    cursor = db.cursor()
    sql = "select * from user where name='%s'"%name
    cursor.execute(sql)

    r = cursor.fetchone()
    print(r)

    if r !=None:
        c.send(b'EXISTS')
        return
    sql = "insert into user (name,passwd) values('%s','%s')"%(name,pwd)
    try:
        cursor.execute(sql)
        db.commit()
        c.send('OK'.encode())
    except:
        db.rollback()
        c.send('FALL'.encode())
        return
    else:
        print('%s注册成功'%name)
def do_query(c,db,data):
    l = data.split(' ')
    word = l[1]
    name = l[2]
    cursor = db.cursor()
    sql = "select hanyi from dict_l where name = '%s'"%word
    cursor.execute(sql)

    r = cursor.fetchone()
    if r == None:
        c.send('None'.encode())
    else:
        print(666)
        in_hist(c,db,name,word)
        s=str(r)
        c.send(s.encode())
def in_hist(c,db,name,word):
    print(777)
    cursor = db.cursor()
    sql = "insert into hist(name,word) values('%s','%s')"%(name,word)
    cursor.execute(sql)
    db.commit()
    print(888)
    
def do_hist(c,db,data):
    l = data.split(' ')
    name = l[1]
    cursor = db.cursor()
    sql = "select word from hist where name='%s'"%name
    cursor.execute(sql)
    r = cursor.fetchall()
    print(r)
    if r == ():
        c.send('None'.encode())
    else:
        s = str(r)
        c.send(s.encode())



if __name__ == '__main__':
    main()