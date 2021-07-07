import ctypes
import os
import time

import win32process
from win32com.client import Dispatch

from tools import dm
from tools.DmTools import *
import GlobalVar as gl


class DnfModel():
    dm = None

    def __init__(self):
        self.dm = noRegsvr()
        # self.dm2 = noRegsvr()l

    def initWindow(self, title="地下城与勇士", num=4, isKill=0):
        hwnd = FindWindow(self.dm, title, num, isKill)
        if (hwnd != 0):
            self.dm.MoveWindow(hwnd, 0, 0)
            self.dm.SetWindowState(hwnd, 1)

    def current(self, item):
        self.clear()
        if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
            self.dm.KeyPress(76)
            time.sleep(1)
        time.sleep(1)
        ret = ocrJb(self.dm)
        if (ret != -1 and int(ret) < 500000000):
            self.upSell(item)  # 上架
        self.exchangeId(item)

    def exchangeId(self, item):
        self.clear()
        self.dm.KeyPress(27)  # 换角色
        time.sleep(1)
        clickPic(self.dm, "dnfimg/选择角色.bmp", 200, 1, 351, 422, 410, 471)
        time.sleep(2)

        if (findPic(self.dm, "dnfimg/id2.bmp", 300, 0, 148,438,258,516)[0] == 0):
            MoveTo(self.dm, 72, 462)
            LeftClick(self.dm)
        else:
            MoveTo(self.dm, 202, 462)
            LeftClick(self.dm)

        clickPic(self.dm, "dnfimg/游戏开始.bmp", 2000)
        time.sleep(5)
        findPic(self.dm, "dnfimg/拍卖行.bmp", 3000, 1, 769, 555, 807, 592)

    def login(self, data):
        self.initWindow("地下城与勇士", 3, 0)
        if (findPic(self.dm, "dnfimg/拍卖行.bmp", 10, 0, 769, 555, 807, 592)[0] == 0):
            return

        hd = FindWindow(self.dm, "WeGame", 2, 0)
        if (hd == 0):
            win32process.CreateProcess('D:\\Program Files (x86)\\WeGame\\wegame.exe', '', None, None, 0,
                                       win32process.CREATE_NO_WINDOW,
                                       None, None, win32process.STARTUPINFO())
            time.sleep(3)
            self.initWindow("WeGame", 15, 1)
            clickPic(self.dm, "dnfimg/wg首页.bmp", 200, 0, 0, 0, 1300, 1200)
            clickPic(self.dm, "dnfimg/wg地下城.bmp", 200, 0, 0, 0, 1300, 1200)
        else:
            self.initWindow("WeGame", 10, 1)

        clickPic(self.dm, "dnfimg/启动.bmp", 200, 1, 0, 0, 1300, 1200)
        time.sleep(30)
        self.initWindow("地下城与勇士", 30)
        clickPic(self.dm, "dnfimg/游戏开始.bmp", 2000)
        time.sleep(5)
        findPic(self.dm, "dnfimg/拍卖行.bmp", 3000, 1, 769, 555, 807, 592)

    def clear(self):
        self.initWindow()
        self.dm.KeyPress(27)  # 重置一下
        time.sleep(0.1)
        clickPic(self.dm, "dnfimg/首页弹窗关闭.bmp", 10, 0, 343, 432, 457, 480)
        clickPic(self.dm, "dnfimg/关闭.bmp", 10, 0, 578, 103, 638, 144)
        clickPic(self.dm, "dnfimg/关闭拍卖行.bmp", 10, 0, 722, 27, 807, 60)

    def spmhPre(self, item):

        self.clear()
        if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
            self.dm.KeyPress(76)
            time.sleep(1)

        ret = ocrJb(self.dm)    #检查金币数量，金币不足上架，换角色
        if (ret != -1 and int(ret) < 500000):
            gl.set_value("jbIsNotEnoughError", 1)
            print(1)

        MoveTo(self.dm, 43, 67)  # 点击物品搜索tab
        LeftClick(self.dm)

        MoveTo(self.dm, 43, 116)  # 点击全部
        LeftClick(self.dm)

        MoveTo(self.dm, 220, 93)  # 点击输入框
        LeftClick(self.dm)

        for i in range(5):
            self.dm.KeyPress(39)
            time.sleep(0.01)
        for i in range(15):
            self.dm.KeyPress(8)
            time.sleep(0.01)
        SendString(self.dm, item['name'])
        clickPic(self.dm, "dnfimg/搜索.bmp", 300, 1, 627, 69, 686, 109)
        MoveTo(self.dm, 595, 141)  # 移动到价格tip

    def spmSearch(self, item):
        self.dm.KeyPress(13)
        time.sleep(0.0001)

    def doBuyClick(self, item):
        ret = ocrDj(self.dm)
        if (ret != -1 and int(ret) <= item['buyPrice']):
            print("buy:" + str(item['buyPrice']))
            for i in range(2):
                self.dm.LeftClick()
                time.sleep(0.0001)
            self.dm.MoveTo(595, 151)
            time.sleep(0.0001)
            self.dm.LeftClick()
            time.sleep(0.3)

            MoveTo(self.dm, 220, 93)  # 点击输入框，让enter键搜索生效
            time.sleep(0.01)
            for i in range(2):
                LeftClick(self.dm)
                time.sleep(0.01)
            time.sleep(2)
            MoveTo(self.dm, 595, 141)  # 移回到价格tip
        if (ret == -1):
            gl.set_value("doBuyClickThreadError", 1)
            print(1)

    def getMail(self, data):
        self.clear()
        if (findPic(self.dm, "dnfimg/邮件.bmp", 100, 0, 575, 447, 777, 547)[0] == 0):  # 如果有邮件
            clickPic(self.dm, "dnfimg/邮件.bmp", 10, 0, 575, 447, 777, 547)
            clickPic(self.dm, "dnfimg/选择接收.bmp", 100, 0, 232, 433, 348, 494)
            time.sleep(2)
            self.dm.KeyPress(27)  # 重置一下
        if (findPic(self.dm, "dnfimg/邮件.bmp", 100, 0, 575, 447, 777, 547)[0] == 0):  # 如果还有邮件
            clickPic(self.dm, "dnfimg/邮件.bmp", 10, 0, 575, 447, 777, 547)
            clickPic(self.dm, "dnfimg/选择接收.bmp", 100, 0, 232, 433, 348, 494)
            time.sleep(2)
            self.dm.KeyPress(27)  # 重置一下

    def upSell(self, item):
        self.clear()
        if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
            self.dm.KeyPress(76)
            time.sleep(1)
        clickPic(self.dm, "dnfimg/上架拍卖品.bmp", 100, 0, 0, 508, 117, 591)
        ret = findPic(self.dm, "dnfimg/无色.bmp", 10, 0, 728, 371, 769, 396)
        if (ret[0] == 0):  #
            MoveTo(self.dm, ret[1], ret[2])
            LeftDown(self.dm)
            MoveTo(self.dm, 237, 293)
            LeftUp(self.dm)
            LeftClick(self.dm)  # 点确定
            MoveTo(self.dm, 397, 471)

            if (findPic(self.dm, "dnfimg/无色.bmp", 10, 0, 203, 263, 257, 306)[0] == 0):  # 如果无色移动过去成功
                LeftClick(self.dm)
                for i in range(10):
                    self.dm.KeyPress(8)
                    time.sleep(0.01)
                SendString(self.dm, item['sellPrice'])

                ret = ocrsellDj(self.dm)
                if (ret != -1 and int(ret) == item['sellPrice']):
                    MoveTo(self.dm, 372, 508)
                    LeftClick(self.dm)
                    MoveTo(self.dm, 372, 508)
                    LeftClick(self.dm)  # 48小时
                    # clickPic(self.dm, "dnfimg/开始排名.bmp", 100, 0, 249, 560, 339, 596)

        time.sleep(0.1)
        self.dm.KeyPress(27)  # 重置一下
