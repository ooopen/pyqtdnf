import os
import threading
import time
from queue import Queue


q = Queue(maxsize=0)

q.put([82, 459])
q.put([200, 462])

cur = q.get()
q.put(cur)

print(q.queue)
