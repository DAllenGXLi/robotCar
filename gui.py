# -*- coding: utf-8 -*-
# 创建于 2017/2/26 anr

import wx
import client.capture as capture

class GUI(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "Transfromer")

    def display(self, cap):
        self.cap = cap
        cap.SetSize((640, 480))
        self.sizer = wx.GridBagSizer(hgap=5, vgap=5)
        # blankCapText = wx.StaticText(self.blankCapPanel, -1, "This is a blankPanel!", (0, 0), (640, -1))
        self.controlPanel = ControlPanel(self)
        self.infoPanel = InfoPanel(self)
        self.infoPanel.SetBackgroundColour('#0000ff')
        self.sizer.Add(self.cap, pos=(0, 0), span=(12, 14), flag=wx.EXPAND)
        self.sizer.Add(self.controlPanel, pos=(0, 14), span=(4, 1), flag=wx.EXPAND)
        self.sizer.Add(self.infoPanel, pos=(12, 0), span=(6, 14), flag=wx.EXPAND)
        self.SetSizer(self.sizer)
        self.Fit()

    # initCap(xxxx)  用于设置CapturePanel()或其它panel到主布局的第一块panel即pos=(0, 0)
    def initCap(self, capPanel):
        # self.sizer.Detach(self.blankCapPanel)
        # self.blankCapPanel.Destroy()
        # capPanel.SetSize((640, 100))
        self.sizer.Add(capPanel, pos=(0, 0), span=(3, 3), flag=wx.EXPAND)

# ControlPanel设置信息的布局类，将来在按钮的事件中调用winComInput之类的操作模式类
# 由于此类主要用于写控制控件的布局所以还是写在GUI.py文件里
# conSizer垂直布局，装了serSizer服务器信息布局和cliSizer客户端信息布局，以后服务器布局可以直接删除
class ControlPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        conSizer = wx.BoxSizer(wx.VERTICAL)

        # 服务器地址端口输入
        # self.sAddrText 设置服务器地址
        # self.CcaPortText 设置服务器传指令给客户端的端口号
        # self.CcbPortText 设置服务器传图像给客户端的端口号
        # self.TcaPortText 设置服务器传指令给终端的端口号
        # self.TcbPortText 设置服务器和终端图像传输的端口号

        sAddrLabel = wx.StaticText(self, -1, "Server Address init:")
        self.sAddrText = wx.TextCtrl(self, -1)
        self.sAddrText.SetInsertionPoint(0)
        CcaPortLabel = wx.StaticText(self, -1, "Client connect init:")
        self.CcaPortText = wx.TextCtrl(self, -1)
        self.CcaPortText.SetInsertionPoint(0)
        CcbPortLabel = wx.StaticText(self, -1, "Client capture init:")
        self.CcbPortText = wx.TextCtrl(self, -1)
        self.CcbPortText.SetInsertionPoint(0)
        TcaPortLabel = wx.StaticText(self, -1, "Terminal connect init:")
        self.TcaPortText = wx.TextCtrl(self, -1)
        self.TcaPortText.SetInsertionPoint(0)
        TcbPortLabel = wx.StaticText(self, -1, "Terminal capture init:")
        self.TcbPortText = wx.TextCtrl(self, -1)
        self.TcbPortText.SetInsertionPoint(0)
        self.serverButton = wx.Button(self, -1, "Unconnected")
        self.Bind(wx.EVT_BUTTON, self.OnServerClick, self.serverButton)

        serSizer = wx.GridBagSizer(hgap=5, vgap=5)
        serSizer.Add(sAddrLabel, pos=(0, 0), span=(1, 2))
        serSizer.Add(self.sAddrText, pos=(0, 2), span=(1, 2))
        serSizer.Add(CcaPortLabel, pos=(1, 0), span=(1, 2))
        serSizer.Add(self.CcaPortText, pos=(1, 2), span=(1, 2))
        serSizer.Add(CcbPortLabel, pos=(2, 0), span=(1, 2))
        serSizer.Add(self.CcbPortText, pos=(2, 2), span=(1, 2))
        serSizer.Add(TcaPortLabel, pos=(3, 0), span=(1, 2))
        serSizer.Add(self.TcaPortText, pos=(3, 2), span=(1, 2))
        serSizer.Add(TcbPortLabel, pos=(4, 0), span=(1, 2))
        serSizer.Add(self.TcbPortText, pos=(4, 2), span=(1, 2))
        serSizer.Add(self.serverButton, pos=(5, 1), span=(1, 2))
        conSizer.Add(serSizer)

        # 客户端填写的地址端口
        # self.cAddrText 客户端连接服务器的地址
        # self.ConPortText 指令端口
        # self.CapPortText 图像端口
        # 通过self.控件名.GetValue()取得用户填写的数据

        cAddrLabel = wx.StaticText(self, -1, "Server Address:")
        self.cAddrText = wx.TextCtrl(self, -1)
        self.cAddrText.SetInsertionPoint(0)
        ConPortLabel = wx.StaticText(self, -1, "Client connect port:")
        self.ConPortText = wx.TextCtrl(self, -1)
        self.ConPortText.SetInsertionPoint(0)
        CapPortLabel = wx.StaticText(self, -1, "Client capture port:")
        self.CapPortText = wx.TextCtrl(self, -1)
        self.CapPortText.SetInsertionPoint(0)
        self.clientButton = wx.Button(self, -1, "Start")
        self.Bind(wx.EVT_BUTTON, self.OnClientClick, self.clientButton)

        cliSizer = wx.GridBagSizer(hgap=5, vgap=5)
        cliSizer.Add(cAddrLabel, pos=(0, 0), span=(1, 2))
        cliSizer.Add(self.cAddrText, pos=(0, 2), span=(1, 2))
        cliSizer.Add(ConPortLabel, pos=(1, 0), span=(1, 2))
        cliSizer.Add(self.ConPortText, pos=(1, 2), span=(1, 2))
        cliSizer.Add(CapPortLabel, pos=(2, 0), span=(1, 2))
        cliSizer.Add(self.CapPortText, pos=(2, 2), span=(1, 2))
        cliSizer.Add(self.clientButton, pos=(3, 1), span=(1, 2))
        conSizer.Add(cliSizer)

        self.SetSizer(conSizer)
        conSizer.Fit(self)


    # 点击此按钮将设置的服务器地址和4个端口号
    # 应该是在里面调用server文件夹里的capture和command 实例化这两个类
    # com = Command('192.168.10.234')/cap.Capture('192.168.10.234')然后
    # 类名.createTermialServer(端口号)
    def OnServerClick(self, event):
        self.serverButton.SetLabel("Connected")



    def OnClientClick(self, event):
        self.clientButton.SetLabel("Running")

# 信息显示类，暂时给了两行静态文本，并做了垂直布局
class InfoPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizer = wx.BoxSizer(wx.VERTICAL)
        fisrtText = wx.StaticText(self, -1, "first row", (0, 0), (600, -1), wx.ALIGN_CENTER)
        secondText = wx.StaticText(self, -1, "Second row", (0, 30), (100, -1))
        sizer.AddMany([fisrtText, secondText])
        self.SetSizer(sizer)


app = wx.App()
gui = GUI()
cap = capture.CapturePanel(gui, 30)
gui.display(cap)

while not cap.connectServer('192.168.10.234', 8002): # (server_ip, port)
    pass
# gui.initCap(cap)
# cap = CapturePanel(frame, 30)  # (parent, fps=30)
# gui.initCap(cap)
# gui.init..
# if gui.init...:
#     gui.bind...Event()
#
# cap = capture.CapturePanel(30)

gui.Show()
app.MainLoop()