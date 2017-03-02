# -*- coding: utf-8 -*-
# 创建于 2017/2/6 dou

# 此对象继承wx.Panel
# 整合接收cvFrame与client端的显示
# 独占Tcp通讯端口

import wx
import socket
import cv2
import numpy
from tcp import Tcp

class CapturePanel(wx.Panel, Tcp):

    # parent为父容器
    #  fps为本窗口刷新频率
    # fps为窗口时钟设置间隔，触发nextFrame()
    def __init__(self, parent, fps=30):
        Tcp.__init__(self, "capture:")
        wx.Panel.__init__(self, parent)
        # parent.SetSize((640, 480))
        self.fps = fps
        self.timer = wx.Timer(self)
        self.timer.Start(1000. / self.fps)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.NextFrame)


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



    # address，port分别为服务器tcp链接的ip与端口
    # 当链接失败，返回false
    # 当链接成功，返回true，并设置视频尺寸（与图像规格有关）
    def connectServer(self, address, port):
        if Tcp.connectServer(self, address, port):
            self.frame = self.recvFrame()
            height, width = self.frame.shape[:2]
            self.bmp = wx.BitmapFromBuffer(width, height, self.frame)
            return True
        else:
            return False



# example
app = wx.App()
frame = wx.Frame(None)
cap = CapturePanel(frame, 30)  # (parent, fps=30)
while not cap.connectServer('180.76.163.52', 8002): # (server_ip, port)
    pass
frame.Show()
app.MainLoop()
