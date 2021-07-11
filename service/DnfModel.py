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

    currentItem = None
    ob110 = [{"name": "无色小晶块", "min": 10, "buyPrice": 47, "sellPrice": 49}]  # min:分钟
    ob390 = [{"name": "无色小晶块", "min": 10, "buyPrice": 55, "sellPrice": 57}]  # min:分钟

    def __init__(self):
        self.dm = noRegsvr()
        # self.dm2 = noRegsvr()l

    def initWindow(self, title="地下城与勇士", num=4, isKill=0):

        hwnd = FindWindow(self.dm, title, num, isKill)
        if (hwnd != 0):
            self.dm.MoveWindow(hwnd, 0, 0)
            self.dm.SetWindowState(hwnd, 1)
            time.sleep(1)

    def current(self, item):
        ret = self.upSell(item)
        print(ret)

    def exchangeRole(self, item):
        self.clear()
        self.dm.KeyPress(27)  # 换角色
        time.sleep(1)
        clickPic(self.dm, "dnfimg/选择角色.bmp", 200, 1, 351, 422, 410, 471)
        time.sleep(2)

        if (findPic(self.dm, "dnfimg/id2.bmp", 300, 0, 148, 438, 258, 516)[0] == 0):
            print("id2")
            MoveTo(self.dm, 72, 462)
            LeftClick(self.dm)
        else:
            print("id1")
            MoveTo(self.dm, 202, 462)
            LeftClick(self.dm)

        clickPic(self.dm, "dnfimg/游戏开始.bmp", 2000)
        time.sleep(5)
        findPic(self.dm, "dnfimg/拍卖行.bmp", 3000, 1, 769, 555, 807, 592)

    def beforeExchangeId(self, item):
        # 先收邮件
        self.getMail(item)
        if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行
            self.dm.KeyPress(76)
            time.sleep(1)

        ret = ocrJb(self.dm)  # 检查金币数量，金币不足上架
        if (ret != -1 and int(ret) > 5000000):
            print("金币充足，继续扫拍")
            gl.set_value("spmPreThreadTarget", 1)
            return
        self.upSell(item)  # 换角色之前上架一波
        gl.set_value("exchangeIdThreadTarget", 1)

    def exchangeId(self, item):

        hd = FindWindow(self.dm, "WeGame", 2, 0)
        if (hd == 0):
            win32process.CreateProcess('D:\\Program Files (x86)\\WeGame\\wegame.exe', '', None, None, 0,
                                       win32process.CREATE_NO_WINDOW,
                                       None, None, win32process.STARTUPINFO())
            time.sleep(5)

        self.initWindow("WeGame", 15, 1)
        ret = findPic(self.dm, "dnfimg/wg首页.bmp", 200, 0, 0, 0, 1300, 1200)
        if (ret[0] == 0):
            MoveTo(self.dm, ret[1], ret[2])
            LeftClick(self.dm)
            time.sleep(1)

            ret = findPic(self.dm, "dnfimg/wg地下城.bmp", 200, 0, 0, 0, 1300, 1200)
            if (ret[0] == 0):
                MoveTo(self.dm, ret[1], ret[2])
                LeftClick(self.dm)
                time.sleep(1)

        if (findPic(self.dm, "dnfimg/id110.bmp", 300, 0, 1044, 18, 1142, 100)[0] == 0):  # 当前角色

            id = "110"
        elif (findPic(self.dm, "dnfimg/id390.bmp", 300, 0, 1044, 18, 1142, 100)[0] == 0):
            id = "390"
        else:
            id = None
        print("id" + id)
        time.sleep(1)
        clickPic(self.dm, "dnfimg/关闭应用1.bmp", 100, 0, 1198, 747, 1286, 839)
        time.sleep(1)
        clickPic(self.dm, "dnfimg/关闭应用2.bmp", 100, 0, 1001, 693, 1139, 752)
        time.sleep(1)
        clickPic(self.dm, "dnfimg/关闭应用3.bmp", 100, 0, 673, 485, 1187, 788)

        time.sleep(1)  # 点击切换账号
        MoveTo(self.dm, 1094, 53)
        LeftClick(self.dm)
        MoveTo(self.dm, 1088, 281)
        LeftClick(self.dm)
        time.sleep(1)
        self.initWindow("WeGame")
        time.sleep(1)

        if (id == "110"):

            clickPic(self.dm, "dnfimg/390-1.bmp", 200, 0, 613, 160, 868, 394)
            self.currentItem = self.ob110[0]
        elif (id == "390"):
            clickPic(self.dm, "dnfimg/110-1.bmp", 200, 0, 613, 160, 868, 394)
            self.currentItem = self.ob390[0]
        else:
            myexit("没有找到账号信息")

        time.sleep(3)
        self.initWindow("WeGame")
        clickPic(self.dm, "dnfimg/wg首页.bmp", 200, 0, 0, 0, 1300, 1200)
        clickPic(self.dm, "dnfimg/wg地下城.bmp", 200, 0, 0, 0, 1300, 1200)
        clickPic(self.dm, "dnfimg/协议.bmp", 200, 1, 0, 0, 1300, 1200)
        clickPic(self.dm, "dnfimg/启动.bmp", 200, 1, 0, 0, 1300, 1200)
        time.sleep(30)
        self.initWindow("地下城与勇士", 30)
        clickPic(self.dm, "dnfimg/游戏开始.bmp", 2000)
        time.sleep(70)
        findPic(self.dm, "dnfimg/拍卖行.bmp", 3000, 1, 769, 555, 807, 592)

    def login(self, data):
        self.initWindow("地下城与勇士", 3, 0)
        self.clear()
        if (findPic(self.dm, "dnfimg/拍卖行.bmp", 10, 0, 769, 555, 807, 592)[0] == 0):
            self.dm.KeyPress(77)
            if (findPic(self.dm, "dnfimg/百思不得.bmp", 10, 0, 156, 204, 344, 303)[0] == 0):
                self.currentItem = self.ob390[0]
            elif (findPic(self.dm, "dnfimg/神的.bmp", 10, 0, 156, 204, 344, 303)[0] == 0):
                self.currentItem = self.ob110[0]
            return

        hd = FindWindow(self.dm, "WeGame", 2, 0)
        if (hd == 0):
            win32process.CreateProcess('D:\\Program Files (x86)\\WeGame\\wegame.exe', '', None, None, 0,
                                       win32process.CREATE_NO_WINDOW,
                                       None, None, win32process.STARTUPINFO())
            time.sleep(3)

        self.initWindow("WeGame", 10, 1)

        ret = findPic(self.dm, "dnfimg/qqlogin.bmp", 50, 0, 576, 212, 933, 471)  # qq登录
        if (ret[0] == 0):
            MoveTo(self.dm, 750, 369)
            time.sleep(0.1)
            LeftClick(self.dm)
            time.sleep(1)

        ret = findPic(self.dm, "dnfimg/390-1.bmp", 10, 0, 613, 160, 868, 394)  # 防止没有默认账号，界面不一样
        if (ret[0] == 0):
            MoveTo(self.dm, ret[1], ret[2])
            LeftClick(self.dm)
            time.sleep(2)
            self.initWindow("WeGame", 10, 1)

        ret = findPic(self.dm, "dnfimg/wg首页.bmp", 80, 0, 0, 0, 1300, 1200)
        if (ret[0] == 0):
            MoveTo(self.dm, ret[1], ret[2])
            LeftClick(self.dm)
            time.sleep(1)

            ret = findPic(self.dm, "dnfimg/wg地下城.bmp", 200, 0, 0, 0, 1300, 1200)
            if (ret[0] == 0):
                MoveTo(self.dm, ret[1], ret[2])
                LeftClick(self.dm)
                time.sleep(1)

        if (findPic(self.dm, "dnfimg/id110.bmp", 10, 0, 1044, 18, 1142, 100)[0] == 0):

            print("110")
        elif (findPic(self.dm, "dnfimg/id390.bmp", 10, 0, 1044, 18, 1142, 100)[0] == 0):
            print("390")
        else:
            myexit("没有找到账号信息")

        clickPic(self.dm, "dnfimg/启动.bmp", 200, 1, 0, 0, 1300, 1200)
        time.sleep(30)
        self.initWindow("地下城与勇士", 30)
        clickPic(self.dm, "dnfimg/游戏开始.bmp", 2000)
        time.sleep(5)
        findPic(self.dm, "dnfimg/拍卖行.bmp", 3000, 1, 769, 555, 807, 592)

        self.clear()
        self.dm.KeyPress(77)
        if (findPic(self.dm, "dnfimg/百思不得.bmp", 10, 0, 156, 204, 344, 303)[0] == 0):
            self.currentItem = self.ob390[0]
        elif (findPic(self.dm, "dnfimg/神的.bmp", 10, 0, 156, 204, 344, 303)[0] == 0):
            self.currentItem = self.ob110[0]
        time.sleep(40)

    def clear(self):
        self.initWindow()
        self.dm.KeyPress(27)  # 重置一下
        time.sleep(0.1)
        clickPic(self.dm, "dnfimg/首页弹窗关闭.bmp", 10, 0, 343, 432, 457, 480)
        MoveTo(self.dm, 511, 150)
        LeftClick(self.dm)
        clickPic(self.dm, "dnfimg/关闭.bmp", 10, 0, 578, 103, 638, 144)
        clickPic(self.dm, "dnfimg/关闭拍卖行.bmp", 10, 0, 722, 27, 807, 60)

    def spmhPre(self, item):
        item = self.currentItem
        if (item == None):
            myexit("currentItem为None")
        self.clear()

        # 换武器检查是否死机
        color1 = self.dm.GetColor(16, 583)
        self.dm.KeyPress(49)
        time.sleep(2)
        color2 = self.dm.GetColor(16, 583)
        if (color1 == color2):
            print("网络错误，换角色")
            gl.set_value("networkError", 1)

        else:
            print("换武器ok")

        if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
            self.dm.KeyPress(76)
            time.sleep(1)

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
        item = self.currentItem
        if (item == None):
            myexit("currentItem为None")
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
            MoveTo(self.dm, 595, 141)  # 移回到价格tip
            ret = ocrJb(self.dm)  # 检查金币数量，金币不足上架，换角色

            if (ret != -1 and int(ret) < 5000000):
                gl.set_value("jbIsNotEnoughError", 1)  # 金币不足触发换角色判断
        ret = self.dm.GetCursorPos()
        if (ret[1] != 595):
            self.dm.MoveTo(595, 141)  # 移回到价格tip

        if (ret == -1):
            gl.set_value("doBuyClickThreadError", 1)
            print(1)

    def getMail(self, data):
        self.clear()
        for i in range(5):
            if (findPic(self.dm, "dnfimg/邮件.bmp", 10, 0, 575, 447, 777, 547)[0] == 0):  # 如果有邮件
                clickPic(self.dm, "dnfimg/邮件.bmp", 5, 0, 575, 447, 777, 547)
                clickPic(self.dm, "dnfimg/选择接收.bmp", 5, 0, 232, 433, 348, 494)
                time.sleep(0.5)
                self.dm.KeyPress(27)  # 重置一下

    def upSell(self, item):
        item = self.currentItem
        if (item == None):
            myexit("currentItem为None")
        self.clear()
        if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
            self.dm.KeyPress(76)
            time.sleep(1)

        clickPic(self.dm, "dnfimg/上架拍卖品.bmp", 100, 0, 0, 508, 117, 591)
        time.sleep(1)

        ret = findPic(self.dm, "dnfimg/装备栏.bmp", 100, 0, 401,0,710,170)
        if (ret[0] == 0):  # 为了点击材料栏
            MoveTo(self.dm, ret[1] + 25, ret[2] + 239)  # 点击材料栏
            time.sleep(0.1)
            LeftClick(self.dm)
            time.sleep(0.1)

        ret = findPic(self.dm, "dnfimg/无色.bmp", 100, 0, 698, 312, 803, 470)
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
                    clickPic(self.dm, "dnfimg/开始排名.bmp", 100, 0, 249, 560, 339, 596)

        time.sleep(0.1)
        self.dm.KeyPress(27)  # 重置一下
