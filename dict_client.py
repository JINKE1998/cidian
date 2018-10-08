from socket import *
import sys


#创建网络连接
def main():
    if len(sys.argv)<3:
        print('argv is error')
        return
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s = socket()
    try:
        s.connect((HOST,PORT))
    except Exception as e:
        print(e)
        return
    while True:
        print('''
            ============Welcome============
            --1.注册     2.登录      3.退出--
            ===============================
            ''')
        cmd = input('输入选项>>')
        if cmd == '1':
            name = do_register(s)
            if name != 1:
                print('注册成功')
            pass
        elif cmd == '2':
            name = do_login(s)
            if name:
                print('登录成功')
                login(s,name)
            else:
                continue
                


        elif cmd == '3':
            s.send('E'.encode())
            print('谢谢使用，再见')
            sys.exit()
        elif not cmd:
            break
        else:
            print('输入命令错误')
def login(s,name):
    while True:
        print('''
            =============查询界面============
            --1.查词   2.历史记录     3.退出--
            ================================
            ''')
        cmd = input('请输入选项>>')
        if cmd == '1':

            do_query(s,name)
        elif cmd == '2':
            do_hist(s,name)
        elif cmd == '3':
            return
def do_query(s,name):
    while True:
        word = input('请输入要查询的单词：')
        if not word:
            break
        msg = "Q {} {}".format(word,name)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == 'None':
            print('没有您要查询的单词')
        else:
            print(data)
def do_hist(s,name):
    print('''
        ==================
             历史记录
        ==================
        ''')
    msg = 'H {}'.format(name)
    s.send(msg.encode())
    data = s.recv(1024).decode()
    if data == 'None':
        print('您目前还没有查询过单词')
    else:
        print(data)


def do_register(s):
    while True:
        name = input('请输入用户名：')
        pwd = str(input('请输入密码：'))
        if (' ' in name) or (' ' in pwd):
            print('用户名及密码不允许有空格')
            continue
        msg = "R {} {}".format(name,pwd)

        s.send(msg.encode())

        data = s.recv(128).decode()

        if data == 'OK':
            return name
        elif data == 'EXISTS':
            print('该用户已存在')
            return 1
        else:
            return 1

def do_login(s):
    while True:
        name = input('请输入用户名：')
        if not name:
            return 0
        pwd = input('请输入密码:')
        msg = "L {} {}".format(name,pwd)
        s.send(msg.encode())
        data = s.recv(128).decode()
        if data == 'OK':
            return name
        elif data == 'None':
            print('该用户不存在,请重新输入')
        elif data == 'pwd error':
            print('密码不正确，请重新输入')
        else:
            print('重新输入')




main()