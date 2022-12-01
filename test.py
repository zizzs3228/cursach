import datetime
import time
import hashlib


print(int(time.time()))
print(time.ctime(time.time()))
print(time.ctime(int(time.time())))

code = '124zizzs3228'

hashcode = hashlib.sha256(code)

print(hashcode)

