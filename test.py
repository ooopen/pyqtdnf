import time

import GlobalVar as gl


gl._init_cache()

gl.set_cache("lastTryDoBuyClickTime",int(time.time()))


a= {0: 0, 47.0: 17113, 48.0: 10281928, 49.0: 11265925}

for k,b in a.items():
    print(k)
    print(b)