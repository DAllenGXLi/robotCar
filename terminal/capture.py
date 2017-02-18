# -*- coding: utf-8 -*-
# 2017/2/7 dou
# 此类用于获取摄像头信息并转码传输到服务器端（tcp）

import socket
import cv2
import numpy
import time

class Capture:

    # CAMERA为摄像头编号
    # IMG_QUILITY为画面质量（0-100）
    # captureInterval为获取画面的间隔时间，即刷新频率，单位为s
    def __init__(self, CAMERA = 0, IMG_QUILITY = 80, captureInterval = 0.01):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.CAMERA, self.IMG_QUILITY = CAMERA, IMG_QUILITY
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), self.IMG_QUILITY]
        self.capture = cv2.VideoCapture(self.CAMERA)
        self.isConnect = False
        self.captureInterval = captureInterval
        self.address = ''
        self.PORT = 0


    # 链接服务器
    # 链接成功返回true，失败返回true，同时设置isConnect属性
    def connectServer(self, address, PORT):

        self.address, self.PORT = address, PORT

        try:
            self.socket.connect((self.address, self.PORT))
        except BaseException:
            self.isConnect = False
            print "terminal socket.connect error!"
            return False
        else:
            self.isConnect = True
            print "terminal socket.connect succeed!"
            return True


    # 断开服务器连接
    def disConnectServer(self):
        if self.isConnect:
            self.socket.close()


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
                self.socket.sendall(str(len(stringData)).ljust(16))
                self.socket.sendall(stringData)
                time.sleep(self.captureInterval)
 
# example
cap = Capture(0) # (CAMERA=0, IMG_QUILITY=80, captureInterval=0.01)
while not cap.connectServer('192.168.10.234', 8001): time.sleep(1) # (server_ip, port)
cap.sendImg()








