import ctypes
import inspect
import os
import re
import time
import traceback

from win32com.client import Dispatch

import GlobalVar as gl
from Model.DnfModel import DnfModel


def noRegsvrVip():
    dm_path = os.path.abspath(os.path.dirname(__file__)) + "/../7.2107"
    dms = ctypes.windll.LoadLibrary(r'%s\DmReg.dll' % dm_path)
    dms.SetDllPathW(r'%s\dm.dll' % dm_path, 0)
    dm = Dispatch('dm.dmsoft')
    dm.SetDict(0, r'%s\dm_soft.txt' % dm_path)
    dm_ret = dm.RegEx("zenghansenad8a4ddff0b85f6eb68fce908eb0d5f5", "hansen",
                      "121.204.252.143|121.204.253.161|125.77.165.62|125.77.165.131")
    if dm_ret != 1:
        print("注册失败,只能使用免费功能")
    else:
        file = "reglog" + time.strftime("%Y-%m-%d", time.localtime()) + ".txt"
        fpath = r'%s\../log/' % dm_path + file
        times = dm.ReadIni("Global", "regTimes", fpath)

        res = 0 if times == '' else times

        dm.WriteIni("Global", "regTimes", int(res) + 1, fpath)
        print("注册成功：" + str(dm_ret))
    return dm


def noRegsvr():
    dm_path = "./3.1233"
    dms = ctypes.windll.LoadLibrary(r'%s\DmReg.dll' % dm_path)
    dms.SetDllPathW(r'%s\dm.dll' % dm_path, 0)
    dm = Dispatch('dm.dmsoft')
    dm.SetDict(0, r'%s\dm_soft.txt' % dm_path)
    print(dm)
    return dm


def regsvr():
    dm_path = os.path.abspath(os.path.dirname(__file__)) + "/../3.1233"
    try:
        dm_1 = Dispatch('dm.dmsoft')
    except Exception:
        os.system(r'regsvr32 /s %s\dm.dll' % dm_path)
        dm_1 = Dispatch('dm.dmsoft')
    return dm_1


def clickPic(self, img, num=10, iskill=0, x1=0, y1=0, x2=1200, y2=800):
    dm = self.getDm()
    i = 0
    MoveTo(dm, 0, 0)
    while (i < num):
        ret = dm.FindPic(x1, y1, x2, y2, img, "000000", 0.9, 0)
        if (-1 != ret[0]):
            mylog(self, "success find：" + img)
            MoveTo(dm, ret[1], ret[2])
            LeftClick(dm)
            return
        else:
            i = i + 1
    mylog(self, "fail to find：" + img)
    if (iskill == 1):
        myexit(self, 1)


def findPic(self, img, num=10, iskill=0, x1=0, y1=0, x2=1200, y2=800, color="000000"):
    dm = self.getDm()
    i = 0
    MoveTo(dm, 0, 0)
    while (i < num):
        ret = dm.FindPic(x1, y1, x2, y2, img, color, 0.9, 0)
        if (-1 != ret[0]):
            mylog(self, "success find：" + img)
            return ret
        else:
            i = i + 1
            time.sleep(0.01)
    mylog(self, "fail to find：" + img)
    if (iskill == 1):
        myexit(self, 1)
    return ret


def findCol(self, num=10, x=0, y=0, color=""):
    dm = self.getDm()
    i = 0
    while (i < num):
        ret = dm.CmpColor(x, y, color, 1)
        if (0 == ret):
            return 0
        else:
            i = i + 1


def findColor(self, num=10, iskill=0, x1=0, y1=0, color1="", x2=0, y2=0, color2=""):
    dm = self.getDm()
    i = 0
    MoveTo(dm, 0, 0)
    while (i < num):
        ret1 = dm.CmpColor(x1, y1, color1, 0.9)
        ret2 = dm.CmpColor(x2, y2, color2, 0.9)
        if (0 == ret1 and 0 == ret2):
            mylog(self, "success find：" + color1 + "|" + color2)
            return 0
        else:
            i = i + 1
            time.sleep(0.01)
    mylog(self, "fail to find：" + color1 + "|" + color2)
    if (iskill == 1):
        myexit(self, 1)
    return -1


def ocrDj(dm):
    i = 0
    while (i < 500):
        ret = dm.Ocr(526, 139, 543, 148, "ffffff-000000", 0.9)
        if ("" != ret):
            return ret
        else:
            i = i + 1
    return -1


def ocrsellDj(dm):
    i = 0
    while (i < 100):
        ret = dm.Ocr(301, 447, 368, 492, "ffffff-000000", 0.9)
        if ("" != ret):
            return ret
        else:
            i = i + 1
            time.sleep(0.01)
    return -1


def ocrJb(dm):
    i = 0
    while (i < 100):
        ret = dm.Ocr(717, 545, 797, 557, "ddc593-020204", 0.9)
        if ("" != ret):
            return ret
        else:
            i = i + 1
            time.sleep(0.01)
    return -1


def ocrWsnum(dm):
    i = 0
    while (i < 100):
        ret = dm.Ocr(717, 357, 780, 395, "ffffff-000000", 0.9)
        if ("" != ret):
            return ret
        else:
            i = i + 1
            time.sleep(0.01)
    return -1


def ocrPmh(dm, x1, y1, x2, y2, color):
    i = 0
    while (i < 50):
        ret = dm.Ocr(x1, y1, x2, y2, color, 0.9)
        if ("" != ret):
            return ret
        else:
            i = i + 1
            time.sleep(0.1)
    return -1


def ocrPmhPage(dm,num):
    i = 0
    while (i < 20):
        ret = dm.Ocr(379,503,398,528, '937639-000000',0.9)
        if (num == int(ret)):
            return int(ret)
        else:
            i = i + 1
            time.sleep(0.1)
    return -1


def ocr2(dm):
    i = 0
    dm.MoveTo(0, 0)
    while (i < 10):
        ret = dm.Ocr(561, 129, 624, 141, "ff3131-1d1c1c", 0.9)
        if ("" != ret):
            return ret
        else:
            i = i + 1
            time.sleep(0.1)
    return -1


def grag(x1, y1, x2, y2):
    MoveTo(x1, y1)
    LeftDown()
    MoveTo(x2, y2)
    LeftUp()


def FindWindow(self, title, num=20, iskill=0):
    dm = self.getDm()
    print(dm)
    i = 0
    while (i < num):
        ret = dm.FindWindow("", title)
        if (0 != ret):
            mylog(self, "success find：" + title)
            return ret
        else:
            i = i + 1
            time.sleep(1)
    mylog(self, "fail to find：" + title)
    if (iskill == 1):
        myexit(self, "没有找到窗口" + title)
    return 0


def MoveTo(dm, x, y):
    dm.MoveTo(x, y)
    time.sleep(0.1)


def LeftDown(dm):
    dm.LeftDown()
    time.sleep(0.1)


def LeftUp(dm):
    dm.LeftUp()
    time.sleep(0.1)


def LeftClick(dm):
    dm.LeftClick()
    time.sleep(0.1)


def SendString(dm, str):
    hwnd = dm.GetForegroundFocus()
    dm.SendString(hwnd, str)
    time.sleep(0.1)


def varname(p):
    for line in inspect.getframeinfo(inspect.currentframe().f_back)[3]:
        m = re.search(r'\bvarname\s*\(\s*([A-Za-z_][A-Za-z0-9_]*)\s*\)', line)
    if m:
        return m.group(1)


def mylog(self, msg):
    msg = str(msg)
    msg = time.strftime("%H:%M:%S", time.localtime()) + ":" + str(msg)

    self.signal1.emit(msg)

    dm = self.getDm()
    print(msg)
    file = "runtime" + time.strftime("%Y-%m-%d", time.localtime()) + ".txt"
    dm.WriteFile("log/" + file, msg + "\r\n")
    # 写日志到数据库
    md = DnfModel()
    arg = (0, msg)
    md.addSyslog(*arg)


def mypricelog(self, id, msg):
    dm = self.getDm()

    msg = time.strftime("%H:%M:%S", time.localtime()) + "-" + str(msg)
    self.signal1.emit(msg)
    print(msg)
    file = str(id) + "-" + time.strftime("%Y-%m-%d", time.localtime()) + ".txt"
    dm.WriteFile("log/" + file, msg + "\r\n")


def myexit(self, code):
    dm = self.getDm()
    mylog(self, code)
    gl.set_value("networkError", 1)
