import os
import threading
import time
from queue import Queue

t1 = time.time()

t2  = time.strftime("%M", time.localtime())

t2 = 10
print(t2)
print(int(t2)%10)