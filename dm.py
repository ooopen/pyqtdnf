import ctypes
import os
import time

from win32com.client import Dispatch


def regsvr():
    dm_path = os.path.abspath(os.path.dirname(__file__)) + "/3.1233"
    try:
        dm_1 = Dispatch('dm.dmsoft')
    except Exception:
        os.system(r'regsvr32 /s %s\dm.dll' % dm_path)
        dm_1 = Dispatch('dm.dmsoft')
    return dm_1


def noregsvr():
    dm_path = os.path.abspath(os.path.dirname(__file__)) + "/3.1233"
    dms = ctypes.windll.LoadLibrary(r'%s\DmReg.dll' % dm_path)
    dms.SetDllPathW(r'%s\dm.dll' % dm_path, 0)
    return Dispatch('dm.dmsoft')


# dm = noregsvr()
dm = regsvr()
print(dm.ver())
# exit(0)
f = open("screen.bmp", mode='r')
print(f)
# time.sleep(2) # 休眠0.1秒

hwnd = dm.FindWindow("", "雷电模拟器")

print(hwnd)

# dm.SetWindowState(hwnd,1)
# dm_ret = dm.BindWindowEx(hwnd, "dx.graphic.opengl", "windows", "windows", "", 0)
# dm_ret = dm.BindWindow(131964, "gdi", "normal", "normal", 0)
# print(dm_ret)

print(dm.GetWindowTitle(hwnd))

dm_ret = dm.Capture(0, 0, 2000, 2000, "screen.bmp")

# dm.MoveTo(100, 100)

ret = dm.FindPic(0, 0, 2000, 2000, "aa.bmp", "000000", 0.9, 0)

dm.MoveTo(ret[1], ret[2])

print(ret)
