import psutil
from typing import List

class ProcessManager:
    
    def __init__(self):
        pass  
        
    def get_processes_list(self) -> List['Process']:
        """Получить список процессов"""
        processes = []
        for p in psutil.process_iter():
            try:
                processes.append(Process(
                    pid=p.pid,
                    name=p.name(),
                    username=p.username()
                ))
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return processes
    
    def get_by_id(self, pid: int) -> object['Process']:
        """Получить процесс по PID"""
        try:
            p = psutil.Process(pid)
            return Process(
                pid=p.pid,
                name=p.name(),
                username=p.username()
            )
        except psutil.NoSuchProcess:
            return None
            
    def get_by_name(self, name: str) -> object['Process']:
        """Получить процесс с указанным именем"""
        for p in psutil.process_iter(['name', 'username']):
            try:
                if p.info['name'] == name:
                    return Process(
                        pid=p.pid,
                        name=p.info['name'],
                        username=p.info['username']
                    )
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return None
        
    def find_by_name(self, processes: List['Process'], name: str) -> List['Process']:
        """Поиск по имени в уже загруженном списке"""
        return [p for p in processes if name.lower() in p.name.lower()]
    
    
class Process:
    
    def __init__(self, pid: int, name: str, username: str):
        self.pid = pid
        self.name = name
        self.username = username
        self.cpu = 0.0
        self.memory = 0.0
        
    def __repr__(self):
        return f"Process(pid={self.pid}, name='{self.name}', user='{self.username}')"
    
    def kill_process(self) -> bool:
        """Завершить процесс"""
        try:
            p = psutil.Process(self.pid)
            p.terminate()
            return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return False
    
    def get_process_stat(self) -> dict:
        """Получить статистику процесса"""
        try:
            p = psutil.Process(self.pid)
            with p.oneshot(): 
                self.cpu = p.cpu_percent()
                memory_info = p.memory_info()
                self.memory = memory_info.rss / 1024 / 1024  # МБ
                
                return {
                    'pid': self.pid,
                    'name': self.name,
                    'cpu_percent': self.cpu,
                    'memory_mb': self.memory,
                    'status': p.status(),
                    'create_time': p.create_time(),
                    'ppid': p.ppid()
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            return {'error': 'Process not accessible'}


#________________MAIN______________________
manager = ProcessManager()  

# печать списка процессов
print("=== Все процессы ===")
processes = manager.get_processes_list()
for p in processes[:5]: 
    print(p)

# Получить 1 процесс по имени
print("\n=== Процесс 'Python' ===")
python_process = manager.get_by_name('Python')
print(python_process)

# Найти в списке по имени
print("\n=== Поиск 'Google' в списке ===")
google_processes = manager.find_by_name(processes, 'Google')
for proc in google_processes[:3]:
    print(proc)

# Получить по ID
print("\n=== Процесс по ID ===")
specific_process = manager.get_by_id(595)
print(specific_process)

# Получить статистику процесса
if specific_process:
    print("\n=== Статистика процесса ===")
    stat = specific_process.get_process_stat()
    print(stat)