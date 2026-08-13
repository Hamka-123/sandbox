#Application / Facade

from data_access.process_repository import ProcessRepository
from services.process_operator import ProcessOperator
from services.process_analyzer import ProcessAnalyzer
from services.process_monitor import ProcessMonitor
from presentation.process_view import ProcessView

class ProcessManager:
    
    def __init__(self):
        self.repository = ProcessRepository()
        self.operator = ProcessOperator(self.repository)
        self.analyzer = ProcessAnalyzer()
        self.monitor = ProcessMonitor(self.repository)
        self.view = ProcessView(self)
        
    def get_process_list(self, count = None):
        """Получить список всех процессов"""
        return self.operator.get_processes_list(count)
    
    def get_accessible_processes(self, count = None):
        """Получить список доступных процессов"""
        return self.operator.get_accessible_processes(count)
    
    def display_processes(self, count=None):
        """Показать процессы через View"""
        processes = self.get_accessible_processes(count)
        self.view.display_processes(processes[:count])
    
    def display_processes_stat(self, count=None):
        """Показать статистику процессов через View"""
        processes = self.get_process_list(count)
        accessible_processes = self.get_accessible_processes(count)
        self.view.display_count(processes, accessible_processes)
    
    def find_processes_by_name(self, name):
        """Найти процессы по имени"""
        processes = self.get_process_list()
        return self.analyzer.find_by_name(processes, name)
    
    def get_top_cpu_processes(self, count=5):
        """Топ процессов по CPU"""
        processes = self.get_process_list()
        return self.analyzer.sort_by_cpu(processes)[:count]
    
    def get_top_memory_processes(self, count=5):
        """Топ процессов по Memory"""
        processes = self.get_process_list(count)
        return self.analyzer.sort_by_memory(processes)[:count]
    
    def kill_process(self, pid):
        """Завершить процесс"""
        process_entity = self.repository.get_by_pid(pid)
        if process_entity:
            return self.operator.kill_process(process_entity)
        return {'success': False, 'message': f'Process {pid} not found'}
    
    def start_monitoring(self, duration=30):
        """Запустить мониторинг"""
        self.monitor.watch_processes(duration=duration)