import ctypes
import os
import time

import mail1
import win32process
from win32com.client import Dispatch

from tools import dm
from tools.Cv2 import SlideCrack
from tools.DmTools import *
import GlobalVar as gl


class DnfModel():
    dm = None

    currentItem = None

    IDs = [
        {"idImg": "dnfimg/神的.bmp", "name": "无色小晶块", "min": 10, "buyPrice": 6, "addPrice": 40, "sellPrice": 48},
        {"idImg": "dnfimg/百思不得.bmp", "name": "无色小晶块", "min": 10, "buyPrice": 3, "addPrice": 50, "sellPrice": 55}
    ]

    def __init__(self):
        self.dm = noRegsvr()
        # self.dm = noRegsvrVip()
        self.dm.SetKeypadDelay("normal", 1)
        self.dm.SetMouseDelay("normal", 1)

    def initWindow(self, title="地下城与勇士", num=4, isKill=0):

        hwnd = FindWindow(self.dm, title, num, isKill)
        if (hwnd != 0):
            self.dm.SetWindowState(hwnd, 1)
            self.dm.MoveWindow(hwnd, 0, 0)
            time.sleep(1)

    def current(self):
        self.dm.MoveTo(596, 148)

    ###type=[login，exchangeId]
    def loginOrExchangeId(self, type="login"):
        print(type)
        hwnd = FindWindow(self.dm, "WeGame", 1)
        if (hwnd == 0):
            type = "login"  # 防止wg已经退出的情况

        if (type == "login"):
            # 重启dnf和wegame
            hwnd = FindWindow(self.dm, "地下城与勇士", 1)
            self.dm.SetWindowState(hwnd, 0)
            hwnd = FindWindow(self.dm, "WeGame", 1)
            self.dm.SetWindowState(hwnd, 0)
            time.sleep(1)
            win32process.CreateProcess('D:\\Program Files (x86)\\WeGame\\wegame.exe', '', None, None, 0,
                                       win32process.CREATE_NO_WINDOW,
                                       None, None, win32process.STARTUPINFO())
            time.sleep(3)
            self.initWindow("WeGame", 10, 1)

        else:
            # 关闭游戏
            self.initWindow("WeGame", 10, 1)
            time.sleep(1)
            clickPic(self.dm, "dnfimg/wg首页.bmp", 100, 0, 0, 0, 1300, 1200)
            clickPic(self.dm, "dnfimg/wg地下城.bmp", 50, 0, 0, 0, 1300, 1200)
            clickPic(self.dm, "dnfimg/关闭应用1.bmp", 50, 1, 1198, 747, 1286, 839)
            clickPic(self.dm, "dnfimg/关闭应用2.bmp", 50, 1, 1001, 693, 1139, 752)
            clickPic(self.dm, "dnfimg/关闭应用3.bmp", 50, 1, 673, 485, 1187, 788)

            # 点击切换账号
            self.initWindow("WeGame", 10, 1)
            time.sleep(1)  # 点击wegame的切换账号
            MoveTo(self.dm, 1094, 53)
            LeftClick(self.dm)
            MoveTo(self.dm, 1088, 281)
            LeftClick(self.dm)
            time.sleep(1)

        # 重启wg后如果wg是已登录状态，则直接启动
        if (type == "login"):
            ret = findPic(self.dm, "dnfimg/wg已登录.bmp", 50, 0, 0, 0, 200, 200)
            if (ret[0] == 0):
                self.startGame()
                return

        # 登录界面
        self.initWindow("WeGame", 10, 1)
        time.sleep(1)
        findColor(self.dm, 10, 1, 821, 218, "5f5f60-000000", 681, 335, "f2c113-000000")  # 找到登录界面

        if (type == "exchangeId"):
            MoveTo(self.dm, 821, 218)
            time.sleep(0.1)
            LeftClick(self.dm)
            time.sleep(0.1)
            MoveTo(self.dm, 739, 273)  # TODO 后续这里考虑做成动态的
            LeftClick(self.dm)
            time.sleep(0.1)
        MoveTo(self.dm, 744, 327)
        LeftClick(self.dm)  # 点击登录
        time.sleep(1)

        # 如果弹出滑动验证码，则处理
        ret = findPic(self.dm, "dnfimg/滑条.bmp", 50, 0, 0, 0, 941, 679)
        if (ret[0] == 0):
            for i in range(8):
                ret = findPic(self.dm, "dnfimg/滑条.bmp", 50, 0, 0, 0, 941, 679)
                MoveTo(self.dm, ret[1], ret[2])
                self.dm.LeftDown()
                time.sleep(0.1)
                MoveTo(self.dm, ret[1] + 170, ret[2])
                time.sleep(0.1)
                self.dm.LeftUp()
                time.sleep(1)
                ret = findPic(self.dm, "dnfimg/滑条err.bmp", 50, 0, 0, 0, 941, 679)
                if (ret[0] != 0):
                    break
                time.sleep(1)
                MoveTo(self.dm, 555, 162)  # 刷新验证码
                time.sleep(0.1)
                LeftClick(self.dm)
                time.sleep(1)
                if (i == 7):
                    myexit(self.dm, "verification code is not auth")

        time.sleep(3)
        self.startGame()

    def startGame(self):
        # 启动游戏
        self.initWindow("WeGame", 4, 1)
        time.sleep(1)
        clickPic(self.dm, "dnfimg/wg首页.bmp", 100, 0, 0, 0, 1300, 1200)
        clickPic(self.dm, "dnfimg/wg地下城.bmp", 50, 0, 0, 0, 1300, 1200)
        clickPic(self.dm, "dnfimg/协议.bmp", 50, 0, 0, 0, 1300, 1200)
        clickPic(self.dm, "dnfimg/启动.bmp", 50, 0, 1, 0, 1300, 1200)
        time.sleep(30)
        self.initWindow("地下城与勇士", 30)
        time.sleep(1)
        clickPic(self.dm, "dnfimg/游戏开始.bmp", 2000)
        time.sleep(1)
        MoveTo(self.dm, 410, 570)
        LeftClick(self.dm)  # 防止没点到开始
        LeftClick(self.dm)  # 防止没点到开始
        time.sleep(10)
        findPic(self.dm, "dnfimg/拍卖行.bmp", 3000, 1, 769, 555, 807, 592)
        time.sleep(45)
        # 准备扫拍
        gl.set_value("spmPreThread", 1)

    def spmhPre(self):

        # 判断当前角色
        self.getMail()
        time.sleep(0.5)
        self.dm.KeyPress(77)
        if (findPic(self.dm, "dnfimg/个人信息.bmp", 50, 0, 181, 2, 315, 125)[0] == -1):
            self.dm.KeyPress(77)

        time.sleep(1)
        for index in range(len(self.IDs)):
            if (findPic(self.dm, self.IDs[index]['idImg'], 10, 0, 156, 204, 344, 303)[0] == 0):
                self.currentItem = self.IDs[index]
                mylog(self.dm, self.currentItem)
                mylog(self.dm, "current id is " + self.IDs[index]['idImg'])
                break
            if (index + 1 == len(self.IDs)):
                mylog(self.dm, "id is not found")
                gl.set_value("spmPreThread", 1)
                return
        if (self.currentItem == None):
            myexit(self.dm, "currentItem为None")

        self.dm.KeyPress(77)  # 关闭角色信息
        time.sleep(0.5)

        self.dm.KeyPress(76)
        time.sleep(1)

        # 判断金币是否充足，否则换角色
        ret = ocrJb(self.dm)  # 检查金币数量，金币不足上架
        print(ret)
        gl.set_value("jbleft", ret)  # 为第一次购买成功计算依据

        if (ret != -1 and int(ret) > 5000000):
            mylog(self.dm, "金币充足，继续扫拍")
            # 继续扫拍
        else:
            self.upSell()
            self.upSell()
            # 更换角色
            mylog(self.dm, "金币不足")
            gl.set_value("JbIsNotEnoughError", 1)
            return

        # 定位到搜索栏
        self.dm.KeyPress(76)
        time.sleep(1)
        MoveTo(self.dm, 43, 67)  # 点击物品搜索tab
        LeftClick(self.dm)
        MoveTo(self.dm, 43, 116)  # 点击全部
        LeftClick(self.dm)
        MoveTo(self.dm, 220, 93)  # 点击输入框
        LeftClick(self.dm)

        # 清空并输入物品名称到搜索栏
        for i in range(5):
            self.dm.KeyPress(39)
            time.sleep(0.01)
        for i in range(15):
            self.dm.KeyPress(8)
            time.sleep(0.01)
        SendString(self.dm, self.currentItem['name'])
        clickPic(self.dm, "dnfimg/搜索.bmp", 300, 1, 627, 69, 686, 109)
        self.dm.MoveTo(368, 548)  # 点击购买准备
        self.dm.LeftCLick()
        MoveTo(self.dm, 595, 141)  # 移动到价格tip

        # 扫拍执行
        gl.set_value("spmSearchThread", 1)
        gl.set_value("doBuyClickThread", 1)

    # 不断输入enter键，持续刷新拍卖行数据
    def spmSearch(self, ):
        self.dm.KeyPress(13)

    def doBuyClick(self):
        item = self.currentItem
        if (item == None):
            myexit(self.dm, "currentItem为None")
        t1 = time.time()
        ret = ocrDj(self.dm)
        # 如果检测到物品价格低于预设，
        if (ret != -1 and int(ret) <= item['buyPrice']):
            # mylog(self.dm,"识别耗时："+str(time.time()-t1))
            self.dm.LeftClick()
            self.dm.MoveTo(595, 151)
            self.dm.LeftClick()
            self.dm.KeyPress(13)
            t2 = time.time()
            msg = time.strftime("%H:%M:%S", time.localtime()) + "单价：" + ret + ";拍卖耗时：" + str(t2 - t1)

            MoveTo(self.dm, 220, 93)  # 点击输入框，让enter键搜索生效
            time.sleep(0.1)
            for i in range(2):
                LeftClick(self.dm)
            time.sleep(0.1)

            self.dm.MoveTo(368, 548)  # 点击购买准备
            time.sleep(0.1)
            self.dm.LeftCLick()
            self.dm.LeftCLick()
            time.sleep(0.1)
            self.dm.MoveTo(595, 141)  # 移回到价格tip
            gl.set_cache("lastTryDoBuyClickTime", int(time.time()))  # 终极大招的判断依据

            retleft = ocrJb(self.dm)  # 检查金币数量，金币不足上架，换角色
            jbleft = gl.get_value("jbleft")
            if (jbleft == retleft):
                status = "失败"
                num = "未知"
            else:
                gl.set_value("jbleft", retleft)
                status = "成功"
                num = (int(jbleft) - int(retleft)) / (item['addPrice'] + int(ret))
            mylog(self.dm, msg + "=>" + "数量：" + str(num) + "|" + status)

            if (retleft != -1 and int(retleft) < 5000000):
                mylog(self.dm, "金币不足")
                gl.set_value("doBuyClickThreadError", 1)  # 金币不足触发上架判断

        ts = time.strftime("%S", time.localtime())
        if (int(ts)  == 50):#防不刷新
            MoveTo(self.dm, 220, 93)  # 点击输入框，让enter键搜索生效
            time.sleep(0.1)
            for i in range(2):
                LeftClick(self.dm)
            time.sleep(0.1)
            self.dm.MoveTo(368, 548)  # 点击购买准备
            time.sleep(0.1)
            self.dm.LeftCLick()
            self.dm.LeftCLick()
            time.sleep(0.1)
            self.dm.MoveTo(595, 141)  # 移回到价格tip

        if (ret == -1):
            mylog(self.dm, "识别单价失败")
            gl.set_value("doBuyClickThreadError", 1)

    def getMail(self):
        self.clear()
        for i in range(10):
            if (findPic(self.dm, "dnfimg/邮件.bmp", 10, 0, 685, 463, 801, 541)[0] == 0):  # 如果有邮件
                clickPic(self.dm, "dnfimg/邮件.bmp", 5, 0, 685, 463, 801, 541)
                clickPic(self.dm, "dnfimg/选择接收.bmp", 5, 0, 232, 433, 348, 494)
                time.sleep(0.5)
                self.dm.KeyPress(27)  # 重置一下
            else:
                break

    def upSell(self):
        item = self.currentItem
        if (item == None):
            myexit(self.dm, "currentItem为None")
        self.clear()
        if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
            self.dm.KeyPress(76)
            time.sleep(1)

        clickPic(self.dm, "dnfimg/上架拍卖品.bmp", 100, 0, 0, 508, 117, 591)
        time.sleep(1)

        ret = findPic(self.dm, "dnfimg/装备栏.bmp", 10, 0, 401, 0, 710, 170)
        if (ret[0] == 0):  # 为了点击材料栏
            MoveTo(self.dm, ret[1] + 25, ret[2] + 239)  # 点击材料栏
            time.sleep(0.1)
            LeftClick(self.dm)
            time.sleep(0.1)

        ret = findPic(self.dm, "dnfimg/无色.bmp", 10, 0, 698, 312, 803, 470)
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

    def warnning(self):

        #换武器
        self.clear()
        time.sleep(1)
        color1 = self.dm.GetColor(9,583)
        self.dm.KeyPress(49)  # 重置一下
        time.sleep(1)
        color2 = self.dm.GetColor(9,583)

        if(color2 == color1):
            file = "runtime" + time.strftime("%Y-%m-%d", time.localtime()) + ".txt"
            # 截图
            self.dm.CaptureJpg(0, 0, 2000, 2000, "./screenshot/screen.jpg", 50)
            mail1.send(subject='Test',
                       text='This is a test!',
                       recipients='375161864@qq.com',
                       sender='1107769317@qq.com',
                       username='1107769317@qq.com',
                       password='mvbvvjyckktojegd',
                       attachments={'screen.jpg': './screenshot/screen.jpg', 'log.txt': './log/' + file},
                       smtp_host='smtp.qq.com')

            mylog(self.dm, "终极大招检查失败")
            gl.set_value("networkError", 1)


    def clear(self):
        self.initWindow()
        self.dm.KeyPress(27)  # 重置一下
        time.sleep(0.1)
        clickPic(self.dm, "dnfimg/首页弹窗关闭.bmp", 10, 0, 343, 432, 457, 480)
        MoveTo(self.dm, 511, 150)
        LeftClick(self.dm)
        clickPic(self.dm, "dnfimg/关闭.bmp", 10, 0, 578, 103, 638, 144)
        clickPic(self.dm, "dnfimg/关闭拍卖行.bmp", 10, 0, 722, 27, 807, 60)
