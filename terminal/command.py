# -*- coding: utf-8 -*- #
#created 2017/2/19 dou

from tcp import Tcp
import time
import serial

# 此类用于接收控制信号
class command(Tcp):

    def __init__(self):
        Tcp.__init__(self, 'command:')
        self.ser = None
        self.isConnectToArduino = False


    def connectToArduino(self, port, baud_rate = 9600, timeout=0.1):
        try:
            self.ser = serial.Serial(port, baud_rate, timeout = timeout)
        except BaseException:
            print "ERROR: terminal connect to Arduino failed!"
            return False
        else:
            self.isConnectToArduino = True
            # 注意，这个时间非常重要，链接arduino后不能立刻收发数据
            time.sleep(2)
            print "terminal connect to Arduino successfully!"
            return True



    def sendToArduino(self, command):
        self.ser.write(command)
        # for test
        print self.ser.readline()


    def run(self):
        while True:
            try:
                command = self.recvall(8)
            except BaseException:
                print "ERROR: recive command failed!"
                self.disconnectServer()
                while not self.connectServer(self.address, self.port):
                    time.sleep(1)
            else:
                self.sendToArduino(command)



com = command()
while not com.connectToArduino('COM3'):
    time.sleep(1)
while not com.connectServer('127.0.0.1', 8004):
    time.sleep(1)
com.run()

