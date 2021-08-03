# encoding: utf-8
import ctypes
import inspect
import random
import threading
import time
from queue import Queue
from threading import Thread

import null as null
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QSystemTrayIcon, QMenu, QAction
from system_hotkey import SystemHotkey

from service.DnfService import DnfService
from tools.DmTools import mylog, varname
from ui.main1 import Ui_Form

import GlobalVar as gl


class MainWindow(QWidget):
    currentItem = null

    demonThread = null
    loginThread = null
    spmPreThread = null
    spmSearchThread = null
    doBuyClickThread = null
    getMailThread = null
    exchangeRoleThread = null
    exchangeIdThread = null
    beforeExchangeIdThread = null
    threadControlThread = null

    currentThread = null

    checkTime = 30 * 60  # 自检时间间隔
    checkPriceTime = 5 * 60  # 长时间没有试图购买，触发加价逻辑判断

    # 界面配置信息，先写死

    signal1 = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.model = DnfService()
        self.model.signal1 = self.signal1

        self.ui.pushButton_3.clicked.connect(lambda: self.start("restart"))
        self.ui.pushButton.clicked.connect(lambda: self.start("admin"))
        self.ui.pushButton_2.clicked.connect(self.testCurrent)

        self.hk_stop = SystemHotkey()
        self.hk_stop.register(('control', 'f10'), callback=lambda x: self.stop("admin"))
        self.hk_stop.register(('control', 'f9'), callback=lambda x: self.start("admin"))

        gl._init()
        gl._init_cache()

        self.signal1.connect(self.updateview)
    def getDm(self):
        return self.model.dm

    def updateview(self, text):  # 更新页面执行
        self.ui.textBrowser.append(text)  # 文本框逐条添加数据
        self.ui.textBrowser.moveCursor(self.ui.textBrowser.textCursor().End)  # 文本框显示到底部

    def testCurrent(self):
        #mylog(self, "start")
        self.currentThread = self.runThread(self.currentThread, self.currentThreadTarget)

    def start(self, admin=None):
        mylog(self, "start")

        # 还原加价标识，防止影响到其他角色或场景
        gl.set_cache("changePrice", False)
        gl.set_cache("lastTryDoBuyClickTime", int(time.time()))  # 初始化，第一次判断不进来的问题，解决终极大招的判断依据

        # 还原加价标识，防止影响到其他角色或场景
        gl.set_cache("changePrice", False)

        self.demonThread = self.runThread(self.demonThread, self.demonThreadTarget)
        self.threadControlThread = self.runThread(self.threadControlThread, self.threadControlThreadTarget)

        if (admin == "restart"):
            gl.set_value("loginThread", 1)  # 重启
        if (admin == "admin"):
            gl.set_value("spmPreThread", 1)  # 默认从扫拍开启

    def loginThreadTarget(self):
        self.model.loginOrExchangeId("login")

    def exchangeRoleThreadTarget(self):
        self.model.exchangeRole()

    def exchangeIdThreadTarget(self):

        self.model.loginOrExchangeId("exchangeId")

    def spmPreThreadTarget(self):
        st = gl.get_cache("exchangeIdTime")
        if (st == 0):
            gl.set_cache("exchangeIdTime", int(time.time()))
        self.model.spmhPre()

    def spmSearchThreadTarget(self):
        while (1):
            self.model.spmSearch()

    def doBuyClickThreadTarget(self):
        while (1):
            self.model.doBuyClick()

    def currentThreadTarget(self):
        self.model.current()

    def threadControlThreadTarget(self):

        arr = ["loginThread", "exchangeRoleThread", "exchangeIdThread", "spmPreThread", "spmSearchThread",
               "doBuyClickThread"]

        while (1):
            time.sleep(1)
            for item in arr:
                if (gl.get_value(item) == 1):
                    exec("self." + item + "=self.runThread(self." + item + ", self." + item + "Target)")
                    gl.set_value(item, 0)

    def demonThreadTarget(self):
        while (1):
            time.sleep(1)

            # 终极大招，以试图抢购为依据，判断物价过高，或者金币不足，或者脚本异常,发邮件告警。
            stime = gl.get_cache("lastTryDoBuyClickTime")
            etime = int(time.time())
            if (stime != 0 and etime - stime > self.checkTime and etime - stime < self.checkTime + 5):
                self.stop()
                mylog(self, "抢购异常")
                self.model.warnning()
                self.stop()
                gl.set_value("loginThread", 1)
                time.sleep(5)
            # 5分钟没有试图抢拍，说明效率不高，切换账号
            stime = gl.get_cache("lastTryDoBuyClickTime")
            etime = int(time.time())
            if (stime != 0 and etime - stime > 300 and etime - stime < 305):
                self.stop()
                mylog(self, "5分钟没有试图扫拍，切换账号")
                self.stop()
                gl.set_value("exchangeIdThread", 1)
                time.sleep(5)

            if (gl.get_value("doBuyClickThreadError") == 1):  # 扫拍异常修复
                mylog(self, "doBuyClickThreadError")
                self.stop()
                tm = time.strftime("%M", time.localtime())
                th = time.strftime("%H", time.localtime())
                if (int(th) == 0 and int(tm) < 10):  # 凌晨0点才用
                    gl.set_value("spmPreThread", 1)
                else:
                    self.model.fastSpmPre()

            if (gl.get_value("JbChangeId") == 1):  # 换id
                mylog(self, "JbChangeId")
                self.stop()
                self.model.getMail()
                self.model.upSell()
                self.model.upSell()
                gl.set_value("exchangeIdThread", 1)

            if (gl.get_value("JbChangeRole") == 1):  # 换role
                mylog(self, "JbChangeRole")
                self.stop()
                gl.set_value("exchangeRoleThread", 1)

            if (gl.get_value("networkError") == 1):  # 网络错误，直接重启
                mylog(self, "networkError")
                self.stop()
                gl.set_value("loginThread", 1)

            # 加价逻辑，以试图抢购为依据，如果长时间没有抢购，触发加价判断
            # stime = gl.get_cache("lastTryDoBuyClickTime")
            # etime = int(time.time())
            # if (stime != 0 and etime - stime > self.checkPriceTime and etime - stime < self.checkPriceTime + 2):
            #     mylog(self, "触发加价判断")
            #     self.stop()
            #
            #     self.model.changePrice()
            #     gl.set_value("spmPreThread", 1)
            #     time.sleep(3)

    def stop(self, items=null):  # 停止子线程
        mylog(self, "stop")
        gl._init()
        if (items == null):
            items = [self.loginThread, self.spmPreThread, self.spmSearchThread, self.doBuyClickThread,
                     self.currentThread, self.exchangeIdThread]
        if (items == "admin"):
            items = [self.demonThread, self.threadControlThread, self.loginThread, self.spmPreThread,
                     self.spmSearchThread, self.doBuyClickThread,
                     self.currentThread, self.exchangeIdThread
                     ]

        for i in items:
            if (i != null and i.is_alive()):
                self._async_raise(i.ident, SystemExit)
        for i in items:  # 杀多一次
            if (i != null and i.is_alive()):
                self._async_raise(i.ident, SystemExit)

    def runThread(self, thread, target):
        mylog(self, "begin " + target.__name__)
        if (thread != null and thread.is_alive()):
            self._async_raise(thread.ident, SystemExit)
            # return thread  # 不重复开启线程
        mylog(self, target.__name__)
        thread = Thread(target=target, name=target.__name__,
                        args=()  # 元组
                        )
        thread.start()
        return thread

    def threadTarget(self, func, once=True, data=null):
        if (once):
            func(data)
        else:
            while (1):
                func(data)  # 执行具体业务

    def _async_raise(self, tid, exctype):
        """Raises an exception in the threads with id tid"""
        if not inspect.isclass(exctype):
            raise TypeError("Only types can be raised (not instances)")
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), ctypes.py_object(exctype))
        if res == 0:
            raise ValueError("invalid thread id")
        elif res != 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")


app = QApplication([])
stats = MainWindow()
stats.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
stats.show()
app.exec_()
