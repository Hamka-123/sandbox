#input stop time seconds
#print countdown timer + beep (mac)
#stop after stop time

from time import sleep
from datetime import datetime
import os
import platform

stop_time = int(input("Enter stop time in seconds: "))
'''
print("before sleep")
sleep(5)
print("after sleep")
'''

while stop_time > 0:
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    # Cross-platform beep
    if platform.system() == "Windows":
        import winsound
        winsound.Beep(1000, 200)
    elif platform.system() == "Darwin":
        os.system('say "beep"')
    else:
        print('\a')
    print(f"Time left: {stop_time} seconds")
    sleep(1)
    stop_time -= 1
    
print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("Timer finished!")
