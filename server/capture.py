# -*- coding: utf-8 -*-
# 创建于 2017/2/6 dou
# 修改于 2017/2/12 dou
#
# 此类用于接收并转发实时图像信息

import socket
import time

class Capture:

    # 只需绑定本机ip
    def __init__(self, address):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.terminalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.frame = None
        self.clientConn = None
        self.TerminalConn = None
        self.clientAddr = None
        self.terminalAddr = None


    # 创建client端的tcp监听
    def creatClientServer(self, port):
        try:
            self.clientPort = port
            self.clientSocket.bind((self.address, self.clientPort))
        except BaseException:
            print "client server bind error!"
            return False
        else:
            print "client server bind succees!"
            self.clientSocket.listen(True)
            return True


    # 创建terminal端的tcp监听
    def createTermialServer(self, port):
        try:
            self.terminalPort = port
            self.terminalSocket.bind((self.address, self.terminalPort))
        except BaseException:
            print "terminal server bind error!"
            return False
        else:
            print "terminal server bind succees!"
            self.terminalSocket.listen(True)
            return True


    # 接收数据
    # conn为接收的tcp链接对象，count为接收字节数
    def recvall(self, conn, count):
        buf = b''
        while count:
            try:
                newbuf = conn.recv(count)
            except BaseException:
                print "terminal connect fail!"
                return False
            else:
                if not newbuf: return None
                buf += newbuf
                count -= len(newbuf)
        return buf


    def waitForClient(self):
        print "waitting for client's linking..."
        self.clientConn, self.clientAddr = self.clientSocket.accept()
        print "client link successful!"


    def waitForTerminal(self):
        print "waitting for terminal's linking..."
        self.terminalConn, self.terminalAddr = self.terminalSocket.accept()
        print "terminal link successful!"


    # 从terminal获取frame
    # 前提是已经链接terminal，terminal正常发送数据，否则返回False
    def recvFrame(self):
        length = self.recvall(self.terminalConn, 16)
        if not length:
            return False
        frame = self.recvall(self.terminalConn, int(length))
        if not frame:
            return False
        return frame


    def sendFrame(self, frame):
        try:
            self.clientConn.sendall(str(len(frame)).ljust(16))
            self.clientConn.sendall(frame)
        except BaseException:
            print "client connect failed!"
            return False
        else:
            return True



    # 通过while循环
    # 接收terminal数据，同时传输到Client
    # 接收与发送步骤一致，先接收/发送 数据 字节位数，再接收/发送 数据
    def runServer(self):
        self.waitForClient()
        self.waitForTerminal()
        while True:
            frame = self.recvFrame()
            if not frame:
                self.waitForTerminal()
                continue
            if not self.sendFrame(frame):
                self.waitForClient()
                continue
            time.sleep(0.001)


# example
cap = Capture('127.0.0.1') # (ip)
cap.createTermialServer(8001) # (terminal_port)
cap.creatClientServer(8002) # (client_port)
cap.runServer()

