# -*- coding: utf-8 -*-
# 创建于 2017/2/6 dou

# 此对象继承wx.Panel
# 整合接收cvFrame与client端的显示
# 独占Tcp通讯端口

import wx
import socket
import cv2
import numpy

class CapturePanel(wx.Panel):

    # parent为父容器
    #  fps为本窗口刷新频率
    # fps为窗口时钟设置间隔，触发nextFrame()
    def __init__(self, parent, fps=30):
        wx.Panel.__init__(self, parent)
        parent.SetSize((640, 480))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.fps = fps
        self.timer = wx.Timer(self)
        self.timer.Start(1000. / self.fps)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)
        self.isConnect = False


    # ？？
    def OnPaint(self, evt):
        dc = wx.BufferedPaintDC(self)
        dc.DrawBitmap(self.bmp, 0, 0)


    # 窗口时钟绑定事件，触发该事件以切换窗口画面
    def NextFrame(self, event):
        self.frame = self.recvFrame()
        self.bmp.CopyFromBuffer(self.frame)
        self.Refresh()


    # 通过recvall，加工接收二进制数据，加工返回frame
    def recvFrame(self):
        length = self.recvall(16)
        while not length:
            length = self.recvall(16)
            print "can not get data's length!"
            return False
        stringData = self.recvall(int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        frame = cv2.imdecode(data, 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame


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
    # 当链接成功，返回true，并设置视频尺寸（与图像规格有关）
    def connectServer(self, address, port):
        self.address, self.port = address, port

        try:
            self.socket.connect((self.address, self.port))
        except BaseException:
            print 'client connect server fail!'
            return False
        else:
            print 'client conncet server successfully!!'
            self.isConnect = True
            self.frame = self.recvFrame()
            height, width = self.frame.shape[:2]
            self.bmp = wx.BitmapFromBuffer(width, height, self.frame)
            return True


    # 断开服务器连接
    def disconnectServer(self):
        if self.isConnect:
            self.socket.close()


# example
app = wx.App()
frame = wx.Frame(None)
cap = CapturePanel(frame, 30)  # (parent, fps=30)
while not cap.connectServer('127.0.0.1', 8002): # (server_ip, port)
    pass
frame.Show()
app.MainLoop()
