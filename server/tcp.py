# -*- coding: utf-8 -*-
# created 2017/2/18 dou

import socket
import time
import common.info as info

# 此类用于做tcp服务器中转数据类的基类
# 继承此类，只需 tcp.__init__(self, address, process_name="")
# 然后使用 creatClientServer(port), creatTerminalServer(port)创建数据交互窗口
# 然后使用 waitForClient()， waitForTerminal()开始监听
# 然后使用 recvall(conn, count)接受数据，conn = self.clientConn/TerminalConn
# 使用 self.clientConn/TerminalConn.sendall(str) 发送数据

class Tcp(info.Info):
    # 只需绑定本机ip
    def __init__(self, address, process_name = ''):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.terminalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.clientConn = None
        self.TerminalConn = None
        self.clientAddr = None
        self.terminalAddr = None
        self.processName = process_name


    # 创建client端的tcp监听
    def creatClientServer(self, port):
        try:
            self.clientPort = port
            self.clientSocket.bind((self.address, self.clientPort))
        except BaseException:
            print self.processName, "client server bind error!"
            return False
        else:
            print self.processName, "client server bind succees!"
            self.clientSocket.listen(True)
            return True



    # 创建terminal端的tcp监听
    def createTermialServer(self, port):
        try:
            self.terminalPort = port
            self.terminalSocket.bind((self.address, self.terminalPort))
        except BaseException:
            print self.processName, "terminal server bind error!"
            return False
        else:
            print self.processName, "terminal server bind succees!"
            self.terminalSocket.listen(True)
            return True


    def waitForClient(self):
        print self.processName, "waitting for client's linking..."
        self.clientConn, self.clientAddr = self.clientSocket.accept()
        print self.processName, "client link successful!"



    def waitForTerminal(self):
        print self.processName, "waitting for terminal's linking..."
        self.terminalConn, self.terminalAddr = self.terminalSocket.accept()
        print self.processName, "terminal link successful!"



    # 接收数据
    # conn为接收的tcp链接对象，count为接收字节数
    def recvall(self, conn, count):
        buf = b''
        while count:
            try:
                newbuf = conn.recv(count)
            except BaseException:
                print "recv connect fail!"
                return False
            else:
                if not newbuf: return None
                buf += newbuf
                count -= len(newbuf)
        return buf

