# -*- coding: utf-8 -*- #
# created 2017/2/18 dou

import socket
import time
from tcp import Tcp

# 此类用于tcp转发client传输的控制信号

class Command(Tcp):

    def __init__(self, address):
        Tcp.__init__(self, address, "command:")

    def runServer(self):
        self.waitForClient()
        self.waitForTerminal()
        while True:
            command = self.recvall(self.clientConn, 8)

            if not command:
                self.waitForTerminal()
                continue

            try:
                self.terminalConn.sendall(command)
            except BaseException:
                print "ERROR: server.terminalConn.sendall(command) failed!"
                self.waitForTerminal()
                continue
            time.sleep(0.001)



com = Command('127.0.0.1')
com.creatClientServer(8003)
com.createTermialServer(8004)
com.runServer()


