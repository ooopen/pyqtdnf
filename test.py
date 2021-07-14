import time

import GlobalVar as gl


gl._init_cache()

gl.set_cache("lastTryDoBuyClickTime",int(time.time()))


time.sleep(3)


stime = gl.get_cache("lastTryDoBuyClickTime")
etime = int(time.time())
if(etime - stime > 2):
    print("抢购异常")