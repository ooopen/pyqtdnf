import ctypes
import inspect
import os
import re
import time
import traceback

from win32com.client import Dispatch

import GlobalVar as gl


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


def clickPic(dm, img, num=10, iskill=0, x1=0, y1=0, x2=1200, y2=800):
    i = 0
    MoveTo(dm, 0, 0)
    while (i < num):
        ret = dm.FindPic(x1, y1, x2, y2, img, "000000", 0.9, 0)
        if (-1 != ret[0]):
            mylog(dm, time.strftime("%H:%M:%S", time.localtime()) + " success find：" + img)
            MoveTo(dm, ret[1], ret[2])
            LeftClick(dm)
            return
        else:
            i = i + 1
    mylog(dm, time.strftime("%H:%M:%S", time.localtime()) + " fail to find：" + img)
    if (iskill == 1):
        myexit(dm, 1)


def findPic(dm, img, num=10, iskill=0, x1=0, y1=0, x2=1200, y2=800, color="000000"):
    i = 0
    MoveTo(dm, 0, 0)
    while (i < num):
        ret = dm.FindPic(x1, y1, x2, y2, img, color, 0.9, 0)
        if (-1 != ret[0]):
            mylog(dm, time.strftime("%H:%M:%S", time.localtime()) + " success find：" + img)
            return ret
        else:
            i = i + 1
            time.sleep(0.01)
    mylog(dm, time.strftime("%H:%M:%S", time.localtime()) + " fail to find：" + img)
    if (iskill == 1):
        myexit(dm, 1)
    return ret


def findCol(dm, num=10, x=0, y=0, color=""):
    i = 0
    while (i < num):
        ret = dm.CmpColor(x, y, color, 1)
        if (0 == ret):
            return 0
        else:
            i = i + 1


def findColor(dm, num=10, iskill=0, x1=0, y1=0, color1="", x2=0, y2=0, color2=""):
    i = 0
    MoveTo(dm, 0, 0)
    while (i < num):
        ret1 = dm.CmpColor(x1, y1, color1, 0.9)
        ret2 = dm.CmpColor(x2, y2, color2, 0.9)
        if (0 == ret1 and 0 == ret2):
            mylog(dm, time.strftime("%H:%M:%S", time.localtime()) + " success find：" + color1 + "|" + color2)
            return 0
        else:
            i = i + 1
            time.sleep(0.01)
    mylog(dm, time.strftime("%H:%M:%S", time.localtime()) + " fail to find：" + color1 + "|" + color2)
    if (iskill == 1):
        myexit(dm, 1)
    return -1


def ocrDj(dm):
    i = 0
    while (i < 100):
        ret = dm.Ocr(536, 139, 543, 148, "ffffff-000000", 1)
        if ("" != ret):
            return ret
        else:
            i = i + 1
    return -1


def ocrsellDj(dm):
    i = 0
    while (i < 100):
        ret = dm.Ocr(325, 458, 380, 485, "ffffff-000000", 0.9)
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


def FindWindow(dm, title, num=20, iskill=0):
    i = 0
    while (i < num):
        ret = dm.FindWindow("", title)
        if (0 != ret):
            mylog(dm, time.strftime("%H:%M:%S", time.localtime()) + " success find：" + title)
            return ret
        else:
            i = i + 1
            time.sleep(1)
    mylog(dm, time.strftime("%H:%M:%S", time.localtime()) + " fail to find：" + title)
    if (iskill == 1):
        myexit(dm, "没有找到窗口" + title)
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


def mylog(dm, msg):
    print(msg)
    file = "runtime" + time.strftime("%Y-%m-%d", time.localtime()) + ".txt"
    msg = time.strftime("%H:%M:%S", time.localtime()) + ":" + str(msg)
    dm.WriteFile("log/" + file, msg + "\r\n")


def myexit(dm, code):
    mylog(dm, code)
    gl.set_value("networkError", 1)
