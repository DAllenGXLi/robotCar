# -*- coding: utf-8 -*-
# 创建于 2017/2/6 dou
# 修改于 2017/2/12 dou
#
# 此类用于接收并转发实时图像信息

import socket
import time
from tcp import Tcp

class Capture(Tcp):

    # 只需绑定本机ip
    def __init__(self, address):
        Tcp.__init__(self, address, "capture:")
        self.frame = None



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

