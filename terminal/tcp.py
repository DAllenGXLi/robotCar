# -*- coding: utf-8 -*-
# 创建于 2017/2/18 dou
import socket

# 此类用于终端tcp链接服务器，作为基类使用
class Tcp:

    def __init__(self, process_name = ''):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.isConnect = False
        self.processName = process_name


    # 接收数据
    def recvall(self, count):
        buf = b''
        while count:
            newbuf = self.socket.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf



    # address，port分别为服务器tcp链接的ip与端口
    # 当链接失败，返回false
    # 当链接成功，返回true
    def connectServer(self, address, port):
        self.address, self.port = address, port

        try:
            self.socket.connect((self.address, self.port))
        except BaseException:
            print self.processName, 'client connect server fail!'
            return False
        else:
            print self.processName, 'client conncet server successfully!!'
            self.isConnect = True
            return True


    def sendall(self, str):
        self.socket.sendall(str)



    # 断开服务器连接
    def disconnectServer(self):
        if self.isConnect:
            self.socket.close()