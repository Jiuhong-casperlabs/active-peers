# import modules
from threading import *
import time
from stress_conn import start_sidecar

# creating a thread
threads_list = [Thread(target=start_sidecar, args=(x,),
                       daemon=True) for x in range(5)]

# starting of Thread T
[x.start()for x in threads_list]
time.sleep(5)
print('this is Main Thread')
