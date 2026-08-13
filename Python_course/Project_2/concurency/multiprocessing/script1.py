# interprocess communication
# thread - lightweighting 
# spawn vs fork

import multiprocessing
from time import sleep
import time

RED_TEXT = '\u001b[38;2;255;0;0;1m'
GREEN_TEXT = '\u001b[38;2;0;255;0;1m'
RESET_COLOR = '\u001b[0m'

def locked_print(s, lock, color:str | None = RESET_COLOR):
    with lock:
        print(color, end='')
        print(s)
        print(RESET_COLOR, end='')

def worker(task_name, lock, start_time):
    locked_print(f"{time.perf_counter_ns() - start_time:<15}:{multiprocessing.current_process().name=} {task_name=} start",lock, GREEN_TEXT)
    sleep(3)
    locked_print(f"{time.perf_counter_ns() - start_time:<15}:{multiprocessing.current_process().name=} stop", lock, GREEN_TEXT)
    
def main():
    PROCESSES = 10
    MAIN_START_TIME = time.perf_counter_ns()
    PRINT_LOCK = multiprocessing.Lock()
    locked_print(f"{multiprocessing.current_process().name=} START",PRINT_LOCK, RED_TEXT)
    
    processes = [multiprocessing.Process(
        target=worker, 
        kwargs={
            "task_name": f'task_N{i}',
            "lock": PRINT_LOCK,
            "start_time": MAIN_START_TIME
            }
        ) for i in range(PROCESSES)] 
    
    locked_print(f"{time.perf_counter_ns() - MAIN_START_TIME:<15}:{multiprocessing.current_process().name=} Starting process",PRINT_LOCK, RED_TEXT)
    for p in processes: p.start()    
    locked_print(f"{time.perf_counter_ns() - MAIN_START_TIME:<15}:{multiprocessing.current_process().name=} Joining process",PRINT_LOCK, RED_TEXT)
    for p in processes: p.join()
    locked_print(f"{time.perf_counter_ns() - MAIN_START_TIME:<15}:{multiprocessing.current_process().name=} STOP",PRINT_LOCK, RED_TEXT)
    
if __name__ == '__main__': #guard
    main()
     
    
    
import pickle
import multiprocessing

lock = multiprocessing.Lock()
try:
    pickle.dumps(lock)  # ❌ Упадет здесь
    print("Lock can be pickled")
except TypeError as e:
    print(f"ERROR: {e}")  # "cannot pickle '_thread.lock' object"
    
