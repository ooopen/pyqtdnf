import os
import threading
import time


def test():
    print(1)

thread = threading.Thread(target=test,
                          args=()  # 元组
                          )
thread.start()

time.sleep(1)

while(thread.is_alive() == False):
    print(test.__name__)

print(3)

