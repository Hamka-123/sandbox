import logging
import pathlib
import time
import psutil

#============UTILITIES=================
def ns_to_human(timestamp_ns: int) -> str:
        """Форматирование timestamp(ns) в человекочитаемый вид"""
        seconds = timestamp_ns // 1000000000
        ms = (timestamp_ns % 1000000000) // 1000_000
        t = time.localtime(seconds)
        return f"{t.tm_mday:02d}-{t.tm_mon:02d}-{t.tm_year} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}.{ms:03d}"
    
#=================CLASSES=================
class SystemManager:
    
    def __init__(self):
        self.cached_processes:dict[int:list[MyProcess]] = {}
        self.last_scan_time:int
        self.config = {
            "cache_refresh": 1,
            "logger":MyLogger | None,
            
        }
        
    # TO DO deserialize (restore from disk)
    
    def fetch_process_list(self) -> tuple[list[MyProcess], int]:
        """Получить список процессов и timestamp
        - через psutil получает список процессов со всеми доступными полями в psutil.Process 
        - создаёт объект MyProcess
        - возвращает кортеж из: список объектов процессов и timestamp
        """
        # STEP 1: get processes  
        processes = []
        last_cached = time.time_ns()
        for p in psutil.process_iter():
            try:
                p.cpu_times()
                processes.append(MyProcess(p.pid,last_cached))
            except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
                self.config["logger"].warning(f"Process pid:{e} (name: {p.name()}) is NoSuchProcess or AccessDenied")
                continue
        self.config["logger"].info(f"Fetched {len(processes)} processes at {ns_to_human(last_cached)}")
        return processes, last_cached
    
    def set_process_list_to_cache(self) -> None:
        """Cохранить список процессов в кеш
        - cached_processes - словарь списков процессов
        """
        processes, timestamp = self.fetch_process_list()
        
        # STEP 2:  add item to: self.cached_processes
        self.cached_processes[timestamp] = processes
        self.last_scan_time = timestamp
        
        # STEP 3: TO DO write log 
        self.config["logger"].info(f"Cached {len(processes)} processes at {ns_to_human(timestamp)}")
        
        # STEP 4: print to console
        print(f"Cached {len(processes)} processes at timestamp {ns_to_human(timestamp)}")
        return None
    
    def get_process_list_from_cache(self) -> dict:
        """Получить процессы из кеша
        - вернет словарь {timestamp_ns(int):list[obj]}
        """
        return self.cached_processes
    
    def print_processes(self, limit = None):
        """Распечатать процессы
        - limit - сколько процессов обработать
        """
        last_timestamp = max(self.cached_processes.keys())
        processes = self.cached_processes[last_timestamp]
        if limit is not None:
            processes = processes[:limit]

        header = f"{'pid':>5} {'Name':>20} {'user':>20}"
        print("-"*len(header))
        print(header)
        print("-"*len(header))
        for p in processes:
            print(f"{p.pid:>5} {p.name():>20} {p.username():>20}")

class MyProcess(psutil.Process):
    
    def __init__(self, pid = None, last_cached=None):
        super().__init__(pid)
        self.last_cached:int = last_cached
    

class MyLogger(logging.Logger):
    
    def __init__(self, name, level = 0, log_file=None):
        super().__init__(name, level)
            
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.addHandler(console_handler)
        
        if log_file:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.addHandler(file_handler)

    
#==========MAIN===========

logger = MyLogger('SystemManager', log_file=pathlib.Path(__file__).parent / 'system_manager.log')

manager = SystemManager()
manager.config["logger"] = logger

manager.set_process_list_to_cache()
manager.get_process_list_from_cache()
manager.print_processes(20)
#manager.stop() # TO DO Serialize


