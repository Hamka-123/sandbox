#Data Access / Repository

import psutil
from domain.process_entity import ProcessEntity

class ProcessRepository:
    """
    Класс доступа к реальным процессам системы через psutil.
    Преобразует каждый процесс в объект ProcessEntity.
    """
    
    def __init__(self):
        pass
    
    def fetch_all(self , limit:int = None) -> list[ProcessEntity]:
        """Получить все процессы списком ProcessEntity"""
        processes = []
        for proc in psutil.process_iter(attrs=['pid','name','ppid','username','cpu_percent','memory_info','status']):
            if limit and len(processes) >= limit:
                break
            try:
                 # Получаем расширенную информацию (может вызвать AccessDenied)
                # Используем oneshot() для атомарного чтения данных
                with proc.oneshot():
                    # Получаем CPU и память внутри oneshot() контекста
                    cpu_percent = proc.cpu_percent(interval=0.1)
                    memory_info = proc.memory_info()
                    create_time = proc.create_time()
                    
                    process_entity = ProcessEntity(
                        pid=proc.info['pid'],
                        name=proc.info['name'],
                        status=proc.info['status'],
                        ppid=proc.info['ppid'],
                        username=proc.info['username'],
                        cpu_percent=cpu_percent,
                        memory=memory_info,  # pmem объект
                        create_time=create_time,
                        accessible=True  
                    )
                    processes.append(process_entity)
            except psutil.AccessDenied:
                # ЕСЛИ AccessDenied - создаем процесс с accessible=False
                process_entity = ProcessEntity(
                    pid=proc.info['pid'],
                    name=proc.info['name'],
                    status="access_denied",
                    ppid=proc.info['ppid'],
                    username=proc.info['username'],
                    cpu_percent=None, # ← Данные по CPU недоступны
                    memory=None,  # ← память недоступна
                    create_time=proc.create_time(),
                    accessible=False  # ← НЕ доступен!
                )
                processes.append(process_entity)
            except psutil.NoSuchProcess:
                continue
        return processes
    
    def fetch_accessible(self , limit:int = None) -> list[ProcessEntity]:
        """Получить доступные процессы списком ProcessEntity"""
        processes = []
        for proc in psutil.process_iter(attrs=['pid','name','ppid','username','cpu_percent','memory_info','status']):
            if limit and len(processes) >= limit:
                break
            try:
                # Получаем расширенную информацию (может вызвать AccessDenied)
                with proc.oneshot():
                    cpu_percent = proc.cpu_percent(interval=0.1)
                    memory_info = proc.memory_info()
                    create_time = proc.create_time()
                    
                    process_entity = ProcessEntity(
                        pid=proc.info['pid'],
                        name=proc.info['name'],
                        status=proc.info['status'],
                        ppid=proc.info['ppid'],
                        username=proc.info['username'],
                        cpu_percent=cpu_percent,
                        memory=memory_info,  # pmem объект
                        create_time=create_time,
                        accessible=True  
                    )
                    processes.append(process_entity)
            except psutil.AccessDenied:
                #print("Process AccessDenied")
                continue
            except psutil.NoSuchProcess:
                continue
        return processes
        
    def get_by_pid(self, pid: int) -> ProcessEntity | None:
        """Получить один процесс в ProcessEntity"""
        try:
            proc = psutil.Process(pid)
            # Возвращаем ProcessEntity с accessible=True
            with proc.oneshot():
                return ProcessEntity(
                    pid=proc.pid,
                    name=proc.name(),
                    status=proc.status(),
                    ppid=proc.ppid(),
                    username=proc.username(),
                    cpu_percent=proc.cpu_percent(interval=0.1),
                    memory=proc.memory_info(),
                    create_time=proc.create_time(),
                    accessible=True
                )
        except psutil.AccessDenied:
            # Возвращаем ProcessEntity с accessible=False
            return ProcessEntity(
                pid=pid,
                name="Access Denied",
                status="access_denied",
                ppid=proc.ppid(),
                username=proc.username(),
                cpu_percent=None,
                memory=None,
                create_time=proc.create_time(),
                accessible=False
            )
        except psutil.NoSuchProcess:
            return None
        
    def kill_process(self, pid: int) -> dict:
        """Пытается завершить процесс - возвращает результат"""
        try:
            proc = psutil.Process(pid)
            proc.terminate()
            return {'success': True, 'message': f'Process {pid} terminated'}
        except psutil.AccessDenied:
            return {'success': False, 'message': f'Access denied for process {pid}'}
        except psutil.NoSuchProcess:
            return {'success': False, 'message': f'Process {pid} not found'}
    