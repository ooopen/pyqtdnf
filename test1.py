from threading import Thread
import time

from GlobalVar import *

import GlobalVar as gl

def work1():
    gl._init()

    gl.set_value('name', 'cc')
    gl.set_value('score', 90)

def work2():
    #延时一会，保证t1线程中的事情做完
    time.sleep(1)

    name = gl.get_value('name')
    score = gl.get_value('score')

    print("%s: %s" % (name, score))

if __name__=='__main__':

    t1 = Thread(target=work1)
    t1.start()
    t2 = Thread(target=work2)
    t2.start()