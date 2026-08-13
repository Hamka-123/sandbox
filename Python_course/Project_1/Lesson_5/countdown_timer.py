# input seconds
# print every seconds: time left
#stop
from time import perf_counter, perf_counter_ns, process_time, process_time_ns, sleep


seconds = int(input("Enter seconds to countdown: "))
'''
print("Start")
sleep(5)
print("Stop")  





'''
'''
process_time()
process_time_ns()
perf_counter()
perf_counter_ns()
'''

'''
for s in range(seconds):
    print("\a")
    print(f"time left {seconds - s}s")
    sleep(1)
'''

    
#v2
while True:
    if seconds < 0:
        break
    print("\a")
    print(f"time left {seconds}s")
    sleep(1)
    seconds -= 1
    
    


    
        