# -*- coding: utf-8 -*- #
# created 2017/2/18 dou

import socket
import time

# 此类用于tcp转发client传输的控制信号

class Command:

    def __init__(self, address):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.terminalSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = address
        self.clientConn = None
        self.TerminalConn = None
        self.clientAddr = None
        self.terminalAddr = None



