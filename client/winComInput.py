# -*- coding: utf-8 -*- #
#created 2017/2/18 dou

import pythoncom
import pyHook

# 此类从windows中通过监听鼠标键盘获取控制信息
# 其中包括信息的技工处理，最终输出规范的控制协议格式
# str(len(stringData)).ljust(16)
class winComInput:

    def __init__(self, width, height):
        self.width, self.height = width, height
        self.hm = pyHook.HookManager()
        self.hm.KeyDown = self.onKeyboardEvent
        self.hm.MouseAll = self.onMouseEvent




    def onMouseEvent(self, event):
        x, y = event.Position;
        print self.analyseMouseData(x, y)
        return True



    def onKeyboardEvent(self, event):
        pass
        return True



    # 分析当前鼠标位置, 按照笛卡尔坐标系计算坐标值
    # 返回两边电机输出功率的元组
    def analyseMouseData(self, x, y):
        dx = int(((x - self.width/2.0)*2/self.width)*255)
        dy = int(-((y - self.height/2.0)*2/self.height)*255)

        # 计算速度差
        if dy>0:
            if (dx<0):
                right_moto_output = dy
                left_moto_output = right_moto_output+dx
            else:
                left_moto_output = dy
                right_moto_output = left_moto_output-dx
        else:
            if (dx<0):
                right_moto_output = dy
                left_moto_output = right_moto_output-dx
            else:
                left_moto_output = dy
                right_moto_output = left_moto_output+dx

        left_moto_output += 255
        right_moto_output += 255

        lcommand = self.formatData(left_moto_output)
        rcommand = self.formatData(right_moto_output)

        return (lcommand, rcommand)




    # 此函数返回符合协议的控制信号元组，分别为左右moto输出
    def formatData(self, moto_output):
        # 格式化输出
        command = "*110"
        data_4 = int(moto_output / 100)
        data_5 = int(moto_output / 10) - data_4 * 10
        data_6 = int(moto_output) - data_4 * 100 - data_5 * 10
        command += str(data_4)
        command += str(data_5)
        command += str(data_6)
        command += "#"
        return command



    def run(self):
        self.hm.HookMouse()
        self.hm.HookKeyboard()
        pythoncom.PumpMessages()




col = winComInput(1920, 1080)
col.run()