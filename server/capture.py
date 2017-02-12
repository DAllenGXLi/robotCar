# -*- coding: utf-8 -*-
# 2017/2/6 dou
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
            newbuf = conn.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


    # 通过while循环
    # 接收terminal数据，同时传输到Client
    # 接收与发送步骤一致，先接收/发送 数据 字节位数，再接收/发送 数据
    def runServer(self):
        print "waitting for terminal's linking..."
        terminalConn, terminalAddr = self.terminalSocket.accept()
        print "terminal link successful!"

        print "waitting for client's linking..."
        clientConn, clientAddr = self.clientSocket.accept()
        print "client link successful!"

        while True:
            length = self.recvall(terminalConn, 16)
            frame = self.recvall(terminalConn, int(length))
            clientConn.sendall(str(len(frame)).ljust(16))
            clientConn.sendall(frame)
            time.sleep(0.001)


# example
cap = Capture('127.0.0.1') # (ip)
cap.createTermialServer(8001) # (terminal_port)
cap.creatClientServer(8002) # (client_port)
cap.runServer()

