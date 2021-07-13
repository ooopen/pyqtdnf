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

        self.currentItem = None  # 此变量已经废弃

        gl._init()

    def testCurrent(self):
        self.currentThread = self.runThread(self.currentThread, lambda: self.currentThreadTarget(self.currentItem),
                                            "currentThread")
        gl.set_value("currentThreadTarget", 1)  # 开启当前调试线程

    def start(self, admin=None):
        print("start")
        if (admin == "restart"):
            gl.set_value("loginThreadTarget", 1)  # 重启
        if (admin == "admin"):
            gl.set_value("spmPreThreadTarget", 1)  # 默认从扫拍开启

        self.demonThread = self.runThread(self.demonThread, self.demonThreadTarget, "demonThread")

        self.loginThread = self.runThread(self.loginThread, self.loginThreadTarget, "loginThread")

        self.spmPreThread = self.runThread(self.spmPreThread, lambda: self.spmPreThreadTarget(self.currentItem),
                                           "spmPreThread")

        self.spmSearchThread = self.runThread(self.spmSearchThread,
                                              lambda: self.spmSearchThreadTarget(self.currentItem), "spmSearchThread")

        self.doBuyClickThread = self.runThread(self.doBuyClickThread,
                                               lambda: self.doBuyClickThreadTarget(self.currentItem),
                                               "doBuyClickThread")
        self.getMailThread = self.runThread(self.getMailThread, self.getMailThreadTarget, "getMailThread")

        self.exchangeIdThread = self.runThread(self.exchangeIdThread,
                                               lambda: self.exchangeIdThreadTarget(self.currentItem),
                                               "exchangeIdThread")

    def loginThreadTarget(self):
        self.threadTarget(self.model.loginOrExchangeId, "loginThreadTarget", True, [], "login")

    def spmPreThreadTarget(self, item):
        self.threadTarget(self.model.spmhPre, "spmPreThreadTarget", True, [], item)

    def spmSearchThreadTarget(self, item):
        self.threadTarget(self.model.spmSearch, "spmSearchThreadTarget", False, [], item)

    def doBuyClickThreadTarget(self, item):
        self.threadTarget(self.model.doBuyClick, "doBuyClickThreadTarget", False, [], item)

    def getMailThreadTarget(self):
        self.threadTarget(self.model.getMail, "getMailThreadTarget", True, [])


    def exchangeIdThreadTarget(self, item):
        self.threadTarget(self.model.loginOrExchangeId, "exchangeIdThreadTarget", True, [], item)

    def currentThreadTarget(self, item):
        self.threadTarget(self.model.current, "currentThreadTarget", True, [], item)

    def demonThreadTarget(self):
        print("demonThreadTarget")
        while (1):
            if (gl.get_value("doBuyClickThreadError") == 1):  # 扫拍异常修复
                print("doBuyClickThreadError")
                self.stop()
                gl._init()

                gl.set_value("spmPreThreadTarget", 1)

                self.start()

            if (gl.get_value("JbIsNotEnoughError") == 1):  # 换角色
                print("JbIsNotEnoughError")
                self.stop()
                gl._init()

                gl.set_value("exchangeIdThreadTarget", 1)

                self.start()

            if (gl.get_value("networkError") == 1):  # 网络错误，直接换角色
                print("networkError")
                self.stop()
                gl._init()

                gl.set_value("loginThreadTarget", 1)

                self.start()

    def stop(self, items=null):  # 停止子线程
        print("stop")
        if (items == null):
            items = [self.loginThread, self.spmPreThread, self.spmSearchThread, self.doBuyClickThread,
                     self.getMailThread, self.currentThread, self.exchangeIdThread, self.beforeExchangeIdThread]
        if (items == "admin"):
            items = [self.loginThread, self.spmPreThread, self.spmSearchThread, self.doBuyClickThread,
                     self.getMailThread, self.currentThread, self.exchangeIdThread, self.beforeExchangeIdThread,
                     self.demonThread]

        for i in items:
            print(i)
            if (i != null and i.is_alive()):
                self._async_raise(i.ident, SystemExit)
        time.sleep(1)

    def runThread(self, thread, target, threadName):

        if (thread != null and thread.is_alive()):
            return thread  # 不重复开启线程
        thread = Thread(target=target, name=threadName,
                        args=()  # 元组
                        )
        thread.start()
        return thread

    def threadTarget(self, func, sign, once=True, startSigns=[], data=null):
        # print(func.__name__)

        while (1):
            if (gl.get_value(sign) == 0):
                time.sleep(1)
            else:
                if (once):  # 只执行一次，关闭标识
                    gl.set_value(sign, 0)
                # print(func.__name__)
                func(data)  # 执行具体业务
                for item in startSigns:  # 执行完毕，开启下一步线程
                    gl.set_value(item, 1)

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
