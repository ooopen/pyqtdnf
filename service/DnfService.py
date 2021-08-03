import ctypes
import math
import os
import time

import mail1
import win32process
from win32com.client import Dispatch

from Model.DnfModel import DnfModel
from tools import dm
from tools.Cv2 import SlideCrack
from tools.DmTools import *
import GlobalVar as gl


class DnfService():
    dm = None

    cPrice = 600 * 10000
    exchangeIdTime = 1200  # s
    currentItem = None

    product1 = {"name": "无色小晶块", "min": 10, "buyPrice": 50, "sellPrice": 52}
    product2 = {"name": "无色小晶块", "min": 10, "buyPrice": 54, "sellPrice": 56}
    product3 = {"name": "无色小晶块", "min": 10, "buyPrice": 66, "sellPrice": 68}

    IDs = [
        {"id": 1, "idImg": "dnfimg/神的.bmp", "product": product1, "nextRole": None},
        # {"id": 1, "idImg": "dnfimg/php剑魂.bmp", "product": product1, "nextRole": {"x": 332, "y": 455}},
        # {"id": 1, "idImg": "dnfimg/杨雪舞.bmp", "product": product1, "nextRole": {"x": 463, "y": 460}},
        # {"id": 1, "idImg": "dnfimg/mc.bmp", "product": product1, "nextRole": {"x": 78, "y": 450}},
        {"id": 2, "idImg": "dnfimg/百思不得.bmp", "product": product2, "nextRole": None},
        # {"id": 3, "idImg": "dnfimg/探险记.bmp", "product": product3, "nextRole": None},
        {"id": 4, "idImg": "dnfimg/屠夫.bmp", "product": product1, "nextRole": None},
    ]

    def __init__(self):
        self.dm = noRegsvr()
        # self.dm = noRegsvrVip()
        self.dm.SetKeypadDelay("normal", 1)
        self.dm.SetMouseDelay("normal", 1)

        self.db = DnfModel()

    def initWindow(self, title="地下城与勇士", num=4, isKill=0):

        hwnd = FindWindow(self.dm, title, num, isKill)
        if (hwnd != 0):
            self.dm.SetWindowState(hwnd, 1)
            self.dm.MoveWindow(hwnd, 0, 0)
            time.sleep(1)

    def current(self):
        self.clear()
        # 判断当前角色
        self.dm.KeyPress(77)
        if (findPic(self.dm, "dnfimg/个人信息.bmp", 50, 0, 181, 2, 315, 125)[0] == -1):
            self.dm.KeyPress(77)
        time.sleep(1)
        ids = self.db.getConfig()

        for index in range(len(ids)):
            if (findPic(self.dm, ids[index]['idimg'], 10, 0, 187, 182, 339, 315)[0] == 0):
                self.currentItem = ids[index]
                mylog(self.dm, self.currentItem)
                mylog(self.dm, "current id is " + ids[index]['idimg'])
                break
            if (index + 1 == len(ids)):
                mylog(self.dm, "id is not found")
                gl.set_value("networkError", 1)
                return
        if (self.currentItem == None):
            myexit(self.dm, "currentItem为None")

        self.dm.KeyPress(77)  # 关闭角色信息
        time.sleep(0.5)

        # 计算购买的值
        # self.calBuyPrice()
        self.coutSell()

    ###type=[login，exchangeId]
    def loginOrExchangeId(self, type="login"):
        mylog(self.dm, type)
        gl.set_cache("lastTryDoBuyClickTime", int(time.time()))  # 初始化，第一次判断不进来的问题，解决终极大招的判断依据
        hwnd = FindWindow(self.dm, "WeGame", 1)
        if (hwnd == 0):
            type = "login"  # 防止wg已经退出的情况

        if (type == "login"):
            # 重启dnf和wegame
            print("restart wg")
            hwnd = FindWindow(self.dm, "地下城与勇士", 1)
            self.dm.SetWindowState(hwnd, 0)
            hwnd = FindWindow(self.dm, "WeGame", 1)
            self.dm.SetWindowState(hwnd, 0)
            self.dm.SetWindowState(hwnd, 13)
            time.sleep(1)
            win32process.CreateProcess('D:\\Program Files (x86)\\WeGame\\wegame.exe', '', None, None, 0,
                                       win32process.CREATE_NO_WINDOW,
                                       None, None, win32process.STARTUPINFO())
            time.sleep(3)
            self.initWindow("WeGame", 10, 1)

        else:
            self.getMail()
            self.upSell()
            # 记录角色信息日志
            ret = gl.get_cache("logoutjbleft")
            args = (
                self.currentItem['uid'], 2, int(ret))
            self.db.addIdslog(*args)

            # 关闭游戏
            self.initWindow("WeGame", 10, 1)
            time.sleep(1)
            clickPic(self.dm, "dnfimg/wg首页.bmp", 50, 0, 0, 0, 1300, 1200)
            clickPic(self.dm, "dnfimg/wg地下城.bmp", 20, 0, 0, 0, 1300, 1200)
            clickPic(self.dm, "dnfimg/关闭应用1.bmp", 20, 1, 1198, 747, 1286, 839)
            clickPic(self.dm, "dnfimg/关闭应用2.bmp", 20, 1, 1001, 693, 1139, 752)
            clickPic(self.dm, "dnfimg/关闭应用3.bmp", 20, 1, 673, 485, 1187, 788)

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
            MoveTo(self.dm, 755, 308)  # TODO 后续这里考虑做成动态的
            time.sleep(0.1)
            self.dm.WheelDown()  # 滚动到最后一个
            time.sleep(0.3)
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
            time.sleep(2)

        self.startGame()

    def startGame(self):
        # 启动游戏
        self.initWindow("WeGame", 4, 1)
        time.sleep(1)
        for i in range(10):
            ret = findPic(self.dm, "dnfimg/wg已登录.bmp", 10, 0, 0, 0, 200, 200)
            if (ret[0] == 0):
                break
            time.sleep(1)

        clickPic(self.dm, "dnfimg/wg首页.bmp", 20, 0, 0, 0, 1300, 1200)
        clickPic(self.dm, "dnfimg/wg地下城.bmp", 20, 0, 0, 0, 1300, 1200)
        clickPic(self.dm, "dnfimg/协议.bmp", 20, 0, 0, 0, 1300, 1200)
        clickPic(self.dm, "dnfimg/启动.bmp", 20, 1, 0, 0, 1300, 1200)
        MoveTo(self.dm, 1215, 17)
        LeftClick(self.dm)
        time.sleep(20)
        self.initWindow("地下城与勇士", 30)
        time.sleep(10)
        findPic(self.dm, "dnfimg/游戏开始.bmp", 4000, 1)
        MoveTo(self.dm, 67, 443)  # 默认第一个角色
        LeftClick(self.dm)
        MoveTo(self.dm, 410, 570)
        time.sleep(3)
        self.dm.LeftDoubleClick()
        self.dm.LeftDoubleClick()
        time.sleep(5)
        findPic(self.dm, "dnfimg/拍卖行.bmp", 3000, 1, 769, 555, 807, 592)
        # 统计拍卖行行情
        self.coutSell()

        # 还原加价标识，防止影响到其他角色或场景
        gl.set_cache("changePrice", False)

        # 还原定时切换账号
        gl.set_cache("exchangeIdTime", time.time())

        gl.set_cache("lastTryDoBuyClickTime", int(time.time()))  # 初始化，第一次判断不进来的问题，解决终极大招的判断依据

        time.sleep(15)
        # 准备扫拍
        gl.set_value("spmPreThread", 1)

    def exchangeRole(self):
        self.clear()
        self.dm.KeyPress(27)  #
        time.sleep(1)
        clickPic(self.dm, "dnfimg/选择角色.bmp", 50, 1, 331, 413, 436, 497)
        findPic(self.dm, "dnfimg/游戏开始.bmp", 2000, 1)
        time.sleep(1)

        MoveTo(self.dm, self.currentItem['nextRole']['x'], self.currentItem['nextRole']['y'], )  # 默认第一个角色
        time.sleep(1)
        LeftClick(self.dm)
        LeftClick(self.dm)
        MoveTo(self.dm, 410, 570)
        LeftClick(self.dm)  # 防止没点到开始
        LeftClick(self.dm)  # 防止没点到开始
        time.sleep(10)
        findPic(self.dm, "dnfimg/拍卖行.bmp", 3000, 1, 769, 555, 807, 592)
        gl.set_value("spmPreThread", 1)

    def spmhPre(self):
        self.getMail()
        self.clear()
        # 判断当前角色
        self.dm.KeyPress(77)
        if (findPic(self.dm, "dnfimg/个人信息.bmp", 50, 0, 181, 2, 315, 125)[0] == -1):
            self.dm.KeyPress(77)
        time.sleep(1)
        ids = self.db.getConfig()

        for index in range(len(ids)):
            if (findPic(self.dm, ids[index]['idimg'], 10, 0, 187, 182, 339, 315)[0] == 0):
                self.currentItem = ids[index]
                mylog(self.dm, self.currentItem)
                mylog(self.dm, "current id is " + ids[index]['idimg'])
                break
            if (index + 1 == len(ids)):
                mylog(self.dm, "id is not found")
                gl.set_value("networkError", 1)
                return
        if (self.currentItem == None):
            myexit(self.dm, "currentItem为None")

        # 记录角色信息日志
        self.clear()
        self.dm.KeyPress(76)
        time.sleep(0.5)
        if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
            self.dm.KeyPress(76)
            time.sleep(0.5)
        ret = ocrJb(self.dm)
        args = (
            self.currentItem['uid'], 1, int(ret))
        self.db.addIdslog(*args)

        # 计算购买的值
        self.calBuyPrice()
        gl.set_cache("lastTryDoBuyClickTime", int(time.time()))  # 初始化，第一次判断不进来的问题，解决终极大招的判断依据
        self.fastSpmPre()

    def fastSpmPre(self):
        self.getMail()
        self.clear()
        self.dm.KeyPress(76)
        time.sleep(0.5)
        for i in range(3):
            if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
                self.dm.KeyPress(76)
                time.sleep(0.5)
            else:
                break

        # 判断金币是否充足，否则换角色
        ret = ocrJb(self.dm)  # 检查金币数量，金币不足上架
        mylog(self.dm, ret)

        gl.set_value("jbleft", ret)  # 为第一次购买成功计算依据

        if (ret != -1 and int(ret) > 5000000):

            mylog(self.dm, "金币充足，继续扫拍")

        else:

            # 更换角色
            mylog(self.dm, "金币不足")
            # 由于金币不足导致的切换，重置切换时间
            gl.set_cache("exchangeIdTime", 0)
            gl.set_value("JbChangeId", 1)

            # 登出前的金币数量
            gl.set_cache("logoutjbleft", int(ret))
            return

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
        SendString(self.dm, self.currentItem['object_name'])
        clickPic(self.dm, "dnfimg/搜索.bmp", 300, 1, 627, 69, 686, 109)
        self.dm.MoveTo(368, 548)  # 点击购买准备
        self.dm.LeftDoubleClick()
        self.dm.LeftDoubleClick()
        MoveTo(self.dm, 595, 141)  # 移动到价格tip

        # 扫拍执行
        gl.set_value("spmSearchThread", 1)
        gl.set_value("doBuyClickThread", 1)

    # 不断输入enter键，持续刷新拍卖行数据
    def spmSearch(self, ):

        self.dm.KeyPress(13)
        time.sleep(self.currentItem['sleep_num'])

    def doBuyClick(self):

        item2 = self.currentItem
        if (item2 == None):
            myexit(self.dm, "currentItem为None")
        item = {}
        for k, v in item2.items():
            item[k] = v

        if (item == None):
            myexit(self.dm, "currentItem为None")

        # #加价逻辑
        if (gl.get_cache("changePrice") == True):
            item['buy_price'] = item['buy_price'] + 1

        t0 = time.time()
        ret = ocrDj(self.dm)

        # 如果检测到物品价格低于预设，
        if (ret != -1 and int(ret) <= item['buy_price']):
            # mylog(self.dm,"识别耗时："+str(time.time()-t1))
            t1 = time.time()
            print(t1 - t0)
            self.dm.LeftClick()
            time.sleep(0.001)
            #self.dm.MoveTo(595, 151)
            #self.dm.LeftClick()
            #self.dm.MoveTo(528,161)
            #time.sleep(0.001)
            #self.dm.LeftClick()
            #self.dm.LeftClick()
            #time.sleep(0.001)
            self.dm.KeyPress(13)
            time.sleep(0.001)
            self.dm.KeyPress(13)
            t2 = time.time()
            msg = time.strftime("%H:%M:%S", time.localtime()) + "单价：" + ret + ";拍卖耗时：" + str(t2 - t1)
            for i in range(5):
                self.dm.KeyPress(13)
                time.sleep(0.001)

            time.sleep(0.7)

            retleft = ocrJb(self.dm)  # 检查金币数量，金币不足上架，换角色
            jbleft = gl.get_value("jbleft")
            if (jbleft == retleft):
                status = "失败"
                is_succ = 0
                num = 0
            else:
                gl.set_value("jbleft", retleft)
                status = "成功"
                is_succ = 1
                num = (int(jbleft) - int(retleft)) / int(ret)
            mylog(self.dm, msg + "=>" + "数量：" + str(num) + "|" + status)

            gl.set_cache("lastTryDoBuyClickTime", int(time.time()))  # 终极大招和涨价的判断依据

            # 写数据库
            buy_scost = int(jbleft) - int(retleft)
            args = (
                self.currentItem['uid'], self.currentItem['id'], is_succ, str(num), buy_scost, int(ret),
                item['buy_price'])
            self.db.addBuylog(*args)

            if (retleft != -1 and int(retleft) < 5000000):
                mylog(self.dm, "金币不足")
                gl.set_value("doBuyClickThreadError", 1)  # 金币不足触发上架判断


            MoveTo(self.dm, 220, 93)  # 点击输入框，让enter键搜索生效
            self.dm.LeftDoubleClick()
            time.sleep(0.1)
            MoveTo(self.dm, 368, 548)  # 点击购买准备
            self.dm.LeftDoubleClick()
            self.dm.MoveTo(595, 141)  # 移回到价格tip

        if (ret == -1):
            mylog(self.dm, "识别单价失败")
            gl.set_value("doBuyClickThreadError", 1)
            time.sleep(3)

        # 定时重启拍卖行，防止鼠标点击问题
        tm = time.strftime("%M", time.localtime())
        ts = time.strftime("%S", time.localtime())
        tms = round(math.modf(float(time.time()))[0], 1)
        if (int(ts) % 10 == 0 and tms < 0.1):
            MoveTo(self.dm, 368, 548)  # 点击购买准备
            self.dm.LeftCLick()
            self.dm.MoveTo(595, 141)  # 移回到价格tip
            if (self.dm.FindPic(627, 69, 686, 109, "dnfimg/搜索.bmp", "000000", 0.9, 0)[0] == 0):  # 如果搜索没有置灰，可能搜索失效
                MoveTo(self.dm, 220, 93)  # 点击输入框，让enter键搜索生效
                self.dm.LeftDoubleClick()
                self.dm.MoveTo(595, 141)  # 移回到价格tip

        # MoveTo(self.dm, 220, 93)  # 点击输入框，让enter键搜索生效
        # self.dm.LeftDoubleClick()
        # self.dm.MoveTo(595, 141)  # 移回到价格tip

        # 定时切换不同账号
        te = int(time.time())
        ts = gl.get_cache("exchangeIdTime")
        if (ts != 0 and te - ts > self.exchangeIdTime):
            gl.set_cache("exchangeIdTime", 0)
            mylog(self.dm, "定时切换账号")
            gl.set_value("JbChangeId", 1)
            time.sleep(3)

    def getMail(self):
        self.clear()
        for i in range(20):
            ret = findPic(self.dm, "dnfimg/邮件.bmp|dnfimg/邮件1.bmp", 1, 0, 685, 463, 801, 541)
            if (ret[0] >= 0):  # 如果有邮件
                MoveTo(self.dm, ret[1], ret[2])
                LeftClick(self.dm)
                time.sleep(0.3)
                MoveTo(self.dm, 305, 469)
                LeftClick(self.dm)
                time.sleep(0.2)
                self.dm.KeyPress(27)  # 重置一下
            else:
                break

    def changePrice(self):
        arr = self.coutSell()

        newPrice = self.currentItem['sell_price'] + 1
        count = 0
        for k, v in arr.items():
            if (v[0] <= newPrice):
                count = count + v[1]
        if (count == 0):
            return
        if (count < self.currentItem['c_price']):
            mylog(self.dm, "目前售价为：" + str(self.currentItem['sell_price']) + ",当前售卖价不大于" + str(newPrice) + "的数量有：" + str(
                count) + ",价格+1")
            gl.set_cache("changePrice", True)
        else:
            mylog(self.dm, "目前售价为：" + str(self.currentItem['sell_price']) + ",当前售卖价不大于" + str(newPrice) + "的数量有：" + str(
                count) + ",不符合加价条件")
            gl.set_cache("changePrice", False)

    def upSell(self):
        item2 = self.currentItem
        print(item2)
        item = {}
        for k, v in item2.items():
            item[k] = v
        if (item2 == None):
            myexit(self.dm, "currentItem为None")
            # 加价逻辑
        if (gl.get_cache("changePrice") == True):
            item['sell_price'] = item['sell_price'] + 1

        self.clear()
        if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
            self.dm.KeyPress(76)
            time.sleep(1)

        clickPic(self.dm, "dnfimg/上架拍卖品.bmp", 100, 0, 0, 508, 117, 591)
        clickPic(self.dm, "dnfimg/上架拍卖品.bmp", 1, 0, 0, 508, 117, 591)
        time.sleep(1)

        ret = findPic(self.dm, "dnfimg/装备栏.bmp", 10, 0, 401, 0, 710, 170)
        if (ret[0] == 0):  # 为了点击材料栏
            MoveTo(self.dm, ret[1] + 25, ret[2] + 239)  # 点击材料栏
            time.sleep(0.1)
            LeftClick(self.dm)
            LeftClick(self.dm)
            LeftClick(self.dm)
            LeftClick(self.dm)
            LeftClick(self.dm)
            LeftClick(self.dm)
            time.sleep(0.1)
        time.sleep(0.5)
        ret = findPic(self.dm, "dnfimg/无色.bmp", 10, 0, 698, 312, 803, 470)
        if (ret[0] == 0):  #

            # 数量大于50万才上架
            num = ocrWsnum(self.dm)
            print(num)
            if (num != -1 and int(num) > 500000):

                MoveTo(self.dm, ret[1], ret[2])
                LeftDown(self.dm)
                MoveTo(self.dm, 237, 293)
                LeftUp(self.dm)
                LeftClick(self.dm)  # 点确定
                LeftClick(self.dm)  # 点确定
                MoveTo(self.dm, 397, 471)

                if (findPic(self.dm, "dnfimg/无色.bmp", 10, 0, 203, 263, 257, 306)[0] == 0):  # 如果无色移动过去成功
                    time.sleep(2)  # 移过去会卡顿有可能
                    LeftClick(self.dm)
                    for i in range(5):
                        self.dm.KeyPress(8)
                        time.sleep(0.01)

                    SendString(self.dm, item['sell_price'])
                    time.sleep(0.5)
                    # 光标移走
                    MoveTo(self.dm, 97, 91)
                    LeftClick(self.dm)
                    LeftClick(self.dm)

                    ret = ocrsellDj(self.dm)
                    print(ret)
                    if (ret != -1 and int(ret) == item['sell_price']):
                        MoveTo(self.dm, 372, 508)
                        LeftClick(self.dm)
                        MoveTo(self.dm, 372, 508)
                        LeftClick(self.dm)  # 48小时
                        clickPic(self.dm, "dnfimg/开始排名.bmp", 100, 0, 249, 560, 339, 596)
                        clickPic(self.dm, "dnfimg/开始排名.bmp", 100, 0, 249, 560, 339, 596)

        time.sleep(0.1)
        self.dm.KeyPress(27)  # 重置一下

    def warnning(self):

        # 换武器
        self.clear()
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
        time.sleep(1)
        color1 = self.dm.GetColor(9, 583)
        self.dm.KeyPress(49)  # 重置一下
        time.sleep(1)
        color2 = self.dm.GetColor(9, 583)
        if (color2 == color1):
            mylog(self.dm, "终极大招检查失败")

    def coutSell(self):
        self.clear()
        for i in range(3):
            if (findPic(self.dm, "dnfimg/个人信息.bmp", 50, 0, 181, 2, 315, 125)[0] == -1):
                self.dm.KeyPress(77)
        ids = self.db.getConfig()
        time.sleep(1)
        for index in range(len(ids)):
            if (findPic(self.dm, ids[index]['idimg'], 10, 0, 156, 204, 344, 303)[0] == 0):
                self.currentItem = ids[index]
                mylog(self.dm, self.currentItem)
                mylog(self.dm, "current id is " + ids[index]['idimg'])
                break

        if (self.currentItem == None):
            myexit(self.dm, "currentItem为None")
        self.clear()

        for i in range(3):
            if (findPic(self.dm, "dnfimg/搜索.bmp", 10, 0, 627, 69, 686, 109)[0] != 0):  # 打开拍卖行，如果没打开
                self.dm.KeyPress(76)
                time.sleep(0.5)
            else:
                break
        time.sleep(1)

        # 定位到搜索栏
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
        SendString(self.dm, self.currentItem['object_name'])
        clickPic(self.dm, "dnfimg/搜索.bmp", 300, 1, 627, 69, 686, 109)
        LeftClick(self.dm)
        time.sleep(1)
        count = 0
        curprice = 0
        arr = {1: [0, 0, 0], 2: [0, 0, 0], 3: [0, 0, 0], 4: [0, 0, 0]}
        ins = 0
        sh = 48
        for i in range(100):
            y1 = 129
            y2 = 141
            yy1 = 125
            yy2 = 140

            yyy1 = 134
            yyy2 = 153

            for i in range(10):
                ret1 = self.dm.Ocr(550, y1, 624, y2, "ffb500-000000|ff3131-000000", 0.9)  # 总价
                y1 = y1 + 37.33333
                y2 = y2 + 37.33333
                ret2 = self.dm.Ocr(142, yy1, 173, yy2, "ffffff-000000|ffce31-000000", 0.9)  # 数量
                yy1 = yy1 + 37.33333
                yy2 = yy2 + 37.33333

                # 最后拍卖剩余时间
                ret3 = self.dm.Ocr(425, yyy1, 444, yyy2, "e1c593-000000", 0.9)
                yyy1 = yyy1 + 37.33333
                yyy2 = yyy2 + 37.33333

                if (ret1 == "" or ret2 == ""):
                    break
                price = int(int(ret1) / int(ret2))
                if (ret1 == "" or ret2 == "" or ins > 4):
                    break

                if (price > curprice):
                    if (count > 0):
                        arr[ins] = [curprice, count, sh]

                    ins = ins + 1
                    count = 0
                    curprice = price
                    sh = 48

                if (int(ret3) < sh):
                    sh = int(ret3)  # 防止48小时造成的误差，取最小为准

                count = count + int(ret2)

            if (ret1 == "" or ret2 == "" or ins > 4):
                break

            self.dm.KeyPress(113)
            time.sleep(1)
        mypricelog(self.dm, self.currentItem['id'], arr)
        # 入库
        if (arr[1][0] == 0):
            return
        args = (
            self.currentItem['id'], self.currentItem['gzone_id'], arr[1][0], arr[1][1], arr[1][2], arr[2][0], arr[2][1],
            arr[2][2], arr[3][0],
            arr[3][1], arr[3][2], arr[4][0], arr[4][1], arr[4][2])
        self.db.addPricetrend(*args)
        return arr

    # 根据历史大数据计算当前应购买价
    def calBuyPrice(self):
        args = (self.currentItem['gzone_id'],)
        data = self.db.getPricetread(*args)
        li = []
        sellh = 0
        sum = 0
        for item in data:
            co = cp = 0
            co = co + item['count1']  # 总数
            if (co < self.currentItem['c_price']):
                cp = item['price1']
                sellh = item['sellh1']
                co = co + item['count2']
                if (co < self.currentItem['c_price']):
                    cp = item['price2']
                    sellh = item['sellh2']
                    co = co + item['count3']
                    if (co < self.currentItem['c_price']):
                        cp = item['price3']
                        sellh = item['sellh3']
                        co = co + item['count4']
                        if (co < self.currentItem['c_price']):
                            cp = item['price4']
                            sellh = item['sellh4']
                        else:
                            co = co - item['count4']

            if (cp == 0):  # count1就比cPrice大了，这时候，应该取cPrice-1
                cp = item['price1'] - 1
            li.append(cp)
            sum = co

        # for i in li:
        #     sum = sum + i
        # sellPrice = sum / ((5 * 10 + 4 + 3 + 2 + 1))
        sellPrice = li[0]
        xs = round(math.modf(sellPrice)[0], 1)
        if (xs > 0.7):
            sellPrice = int(sellPrice) + 1
        else:
            sellPrice = int(sellPrice)

        # 判断销售价最早过期时间，如果低于19小时且总量大于阈值万，则-1
        mylog(self.dm, "不低于价格总量为：" + str(sum))
        if (sellh < 20 and sum > self.currentItem['c_price_min']):

            if (sum == data[0]['count1'] or data[0]['count1'] < 1000000 or (
                    data[0]['count1'] + data[0]['count2']) < 1000000):  # 如果前面都是这个销售价的数据，则放弃-1，因为扫不到
                mylog(self.dm, "目前销售存量基本都是销售价")
            else:
                sellPrice = int(sellPrice) - 1
                mylog(self.dm, "目前销售价存量的最早过期时间为：" + str(sellh) + ",价格-1")
        else:
            mylog(self.dm, "目前销售价存量的最早过期时间为：" + str(sellh))

        mylog(self.dm, "目前存量：" + str(data[0]))
        mylog(self.dm, "大数据智能计算销售价：" + str(sellPrice))

        if (sellPrice > self.currentItem['sell_price']):
            mylog(self.dm, "智能计算的结果为：" + str(sellPrice) + " 大于阈值:" + str(self.currentItem['sell_price']))
            return

        self.currentItem['buy_price'] = sellPrice - 2
        self.currentItem['sell_price'] = sellPrice
        mylog(self.dm, "智能计算结果后的currentItem：" + str(self.currentItem))

    def clear(self):
        self.initWindow()
        self.dm.KeyPress(27)  # 重置一下
        time.sleep(0.1)
        clickPic(self.dm, "dnfimg/关闭首页.bmp|dnfimg/首页弹窗关闭.bmp", 5, 0, 0, 0, 857, 880)
        MoveTo(self.dm, 511, 150)
        LeftClick(self.dm)
        clickPic(self.dm, "dnfimg/关闭.bmp", 5, 0, 578, 103, 638, 144)
        clickPic(self.dm, "dnfimg/关闭契约.bmp", 5, 0, 488, 123, 540, 178)
        clickPic(self.dm, "dnfimg/关闭拍卖行.bmp", 1, 0, 722, 27, 807, 60)
