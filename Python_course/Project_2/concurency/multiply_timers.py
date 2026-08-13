# Timers:

'''
Console print (once a second):

Timer parameter: delay  (millisec, sec)

Timer1  Timer2  Timer3
1          2      33

'''

import os
import threading
import time


times = [0,0,0]

def worker_timer(delay, timer_num):
    while True:
        time.sleep(delay)
        times[timer_num-1] += 1
    
threads = [
    threading.Thread(target=worker_timer, args=(1, 1), daemon=True),
    threading.Thread(target=worker_timer, args=(2, 2), daemon=True),
    threading.Thread(target=worker_timer, args=(5, 3), daemon=True)
]
for thread in threads:
    thread.start()

while True:
    os.system('clear')
    print("Timer1   Timer2   Timer3")
    print("{:<8}{:<8}{:<8}".format(*times))
    time.sleep(1)
    



