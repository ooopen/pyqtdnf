import ctypes
import os

from win32com.client import Dispatch

from tools.DmTools import DmTools


class StzbModel():

    def __init__(self):
        self.dm = DmTools().noRegsvr()
        self.myDm = DmTools()

    def initWindow(self, title):
        hwnd = self.dm.FindWindow("", title)
        self.dm.MoveWindow(hwnd, 0, 0)
        self.dm.SetWindowState(hwnd, 1)


    def conscription(self, now=0):#是否立即征兵
        if (self.myDm.clickPic("bmp/team.bmp") != 1):
            print("打开team界面失败")
            return 0
        if (self.myDm.clickPic("bmp/zn1.bmp") != 1):
            print("打开zn1界面失败")
            return 0
        # if (self.myDm.clickPic("bmp/互换.bmp") != 1):
        #     print("打开互换界面失败")
        #     return 0

        if (now == 1):
            self.myDm.clickPic("bmp/now-btn.bmp")
            self.myDm.clickPic("bmp/jiasu-btn.bmp", 9)

        if (self.myDm.clickPic("bmp/zb-btn.bmp") != 1):
            print("打开zb-btn界面失败")
            return 0

        a = self.myDm.ocr()
        print(123)
        print(a)
        return

        self.myDm.clickPic("bmp/gl-btn.bmp", 3)

        if (now == 1):
            self.myDm.clickPic("bmp/now.bmp", 3)

        ret = self.myDm.findPic("bmp/slide.bmp", 15,1000,220)
        if (ret[0] == -1):
            print("打开slide界面失败")
            return 0
        else:
            pc = 0.1
            self.myDm.grag(ret[1], ret[2], ret[1] + 430 * pc, ret[2])
            self.myDm.grag(ret[1], ret[2] + 95, ret[1] + 428 * pc, ret[2] + 95)
            self.myDm.grag(ret[1], ret[2] + 95 * 2, ret[1] + 430 * pc, ret[2] + 95 * 2)
            self.myDm.clickPic("bmp/确认征兵.bmp", 3)
            self.myDm.clickPic("bmp/征兵-确定.bmp", 10)

    def back(self):
        print("尝试返回界面")
        xxlist = "bmp/close2.bmp|bmp/close.bmp|bmp/back.bmp|bmp/back2.bmp|bmp/征兵-取消.bmp|bmp/back3.bmp"
        if (self.myDm.findPic("bmp/team.bmp")[0] != -1):
            return
        for item in range(0, 4):
            self.myDm.clickPic(xxlist)
