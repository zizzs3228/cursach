import datetime
import time
import hashlib

hour = 1*60*60
print(hour)
print(int(time.time()))
plushour = int(time.time())+hour
print(time.ctime(time.time()))
print(time.ctime(plushour))


