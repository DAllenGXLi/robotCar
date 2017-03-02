# -*- coding: utf-8 -*-
# 2017/2/7 dou
# 此类用于获取摄像头信息并转码传输到服务器端（tcp）

import socket
import cv2
import numpy
import time
from tcp import Tcp

class Capture(Tcp):

    # CAMERA为摄像头编号
    # IMG_QUILITY为画面质量（0-100）
    # captureInterval为获取画面的间隔时间，即刷新频率，单位为s
    def __init__(self, CAMERA = 0, IMG_QUILITY = 80, captureInterval = 0.01):
        Tcp.__init__(self, "capture:")
        self.CAMERA, self.IMG_QUILITY = CAMERA, IMG_QUILITY
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.IMG_QUILITY]
        self.capture = cv2.VideoCapture(self.CAMERA)
        self.captureInterval = captureInterval



    # 获取图像，并且编码
    # return要传输的字符串编码
    def createImg(self):
        ret, frame = self.capture.read()
        if ret:
            result, imgencode = cv2.imencode('.jpg', frame, self.encode_param)
            if result:
                data = numpy.array(imgencode)
                stringData = b'' + data.tostring()
                return stringData
            else:
                print "encode error!"
                return False
        else:
            print "capture.read error!"
            return False


    # 使用while循环传输图像
    def sendImg(self):
        while True:
            stringData = self.createImg()
            if stringData:
                try:
                    self.sendall(str(len(stringData)).ljust(16))
                    self.sendall(stringData)
                    time.sleep(self.captureInterval)
                except BaseException:
                    print self.processName, "send img failed!"
                    self.disconnectServer()
                    while not cap.connectServer(self.address, self.port): time.sleep(1)  # (server_ip, port)
 
# example
cap = Capture(1) # (CAMERA=0, IMG_QUILITY=80, captureInterval=0.01)
while not cap.connectServer('192.168.10.234', 8001): time.sleep(1) # (server_ip, port)
cap.sendImg()








