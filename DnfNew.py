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

from service.DnfModel import DnfModel
from tools.DmTools import mylog
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

    getMailTimes = 60 * 10  # 收邮件和上架的间隔（秒）

    # 界面配置信息，先写死

    def __init__(self):
        super().__init__()

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.model = DnfModel()

        self.ui.pushButton_3.clicked.connect(lambda: self.start("restart"))
        self.ui.pushButton.clicked.connect(lambda: self.start("admin"))
        self.ui.pushButton_2.clicked.connect(self.testCurrent)

        self.hk_stop = SystemHotkey()
        self.hk_stop.register(('control', 'f10'), callback=lambda x: self.stop("admin"))
        self.hk_stop.register(('control', 'f9'), callback=lambda x: self.start("admin"))

        gl._init()
        gl._init_cache()

    def testCurrent(self):
        # self.currentThread = self.runThread(self.currentThread, lambda: self.currentThreadTarget(self.currentItem),
        mylog(self.model.dm, self.loginThreadTarget.__name__)

    def start(self, admin=None):
        mylog(self.model.dm, "start")

        self.demonThread = self.runThread(self.demonThread, self.demonThreadTarget)
        self.threadControlThread = self.runThread(self.threadControlThread, self.threadControlThreadTarget)

        if (admin == "restart"):
            gl.set_value("loginThreadTarget", 1)  # 重启
        if (admin == "admin"):
            gl.set_value("spmPreThreadTarget", 1)  # 默认从扫拍开启

    def loginThreadTarget(self):
        self.model.loginOrExchangeId("login")

    def exchangeIdThreadTarget(self):
        self.model.loginOrExchangeId("exchangeId")

    def spmPreThreadTarget(self):
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

        while (1):
            if (gl.get_value("loginThreadTarget") == 1):
                self.loginThread = self.runThread(self.loginThread, self.loginThreadTarget)
                gl.set_value("loginThreadTarget", 0)

            if (gl.get_value("exchangeIdThreadTarget") == 1):
                self.exchangeIdThread = self.runThread(self.exchangeIdThread, self.exchangeIdThreadTarget)
                gl.set_value("exchangeIdThreadTarget", 0)

            if (gl.get_value("spmPreThreadTarget") == 1):
                self.spmPreThread = self.runThread(self.spmPreThread, self.spmPreThreadTarget)
                gl.set_value("spmPreThreadTarget", 0)

            if (gl.get_value("spmSearchThreadTarget") == 1):
                self.spmSearchThread = self.runThread(self.spmSearchThread, self.spmSearchThreadTarget)
                gl.set_value("spmSearchThreadTarget", 0)

            if (gl.get_value("doBuyClickThreadTarget") == 1):
                self.doBuyClickThread = self.runThread(self.doBuyClickThread, self.doBuyClickThreadTarget)
                gl.set_value("doBuyClickThreadTarget", 0)

    def demonThreadTarget(self):
        mylog(self.model.dm, "demonThreadTarget")
        while (1):
            if (gl.get_value("doBuyClickThreadError") == 1):  # 扫拍异常修复
                mylog(self.model.dm, "doBuyClickThreadError")
                self.stop()
                gl.set_value("spmPreThreadTarget", 1)

            if (gl.get_value("JbIsNotEnoughError") == 1):  # 换角色
                mylog(self.model.dm, "JbIsNotEnoughError")
                self.stop()
                gl.set_value("exchangeIdThreadTarget", 1)

            if (gl.get_value("networkError") == 1):  # 网络错误，直接重启
                mylog(self.model.dm, "networkError")
                self.stop()
                gl.set_value("loginThreadTarget", 1)

            # 终极大招，以试图抢购为依据，判断物价过高，或者金币不足，或者脚本异常,发邮件告警。
            stime = gl.get_cache("lastTryDoBuyClickTime")
            etime = int(time.time())
            if (stime != 0 and etime - stime > 60 * 30):
                mylog(self.model.dm, "抢购异常")
                self.stop()
                gl.set_value("loginThreadTarget", 1)

    def stop(self, items=null):  # 停止子线程
        mylog(self.model.dm, "stop")
        gl._init()
        if (items == null):
            items = [self.loginThread, self.spmPreThread, self.spmSearchThread, self.doBuyClickThread,
                     self.currentThread, self.exchangeIdThread]
        if (items == "admin"):
            items = [self.loginThread, self.spmPreThread, self.spmSearchThread, self.doBuyClickThread,
                     self.currentThread, self.exchangeIdThread, self.threadControlThread,
                     self.demonThread]

        for i in items:
            print(i)
            if (i != null and i.is_alive()):
                self._async_raise(i.ident, SystemExit)

    def runThread(self, thread, target):

        if (thread != null and thread.is_alive()):
            return thread  # 不重复开启线程
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
stats.show()
app.exec_()
