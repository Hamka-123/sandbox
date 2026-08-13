# Presentation / CLI

class ProcessView:
    
    def __init__(self, manager):
        self.manager = manager
    
    def display_processes(self, processes):
        header = f"{'PID':<8} {'Name':<30} {'PPID':<8} {'user':<20} {'CPU%':<6} {'Memory':<12} {'Status':<20} {'Access':<6} {'Create time':<10}"
        print(header)
        print("-" * len(header))
        for process in processes:
            access_icon = "🔒" if not process.accessible else "✅"
            
            # Обрабатываем None в cpu_percent
            cpu_display = "N/A"
            if process.cpu_percent is not None:
                cpu_display = f"{process.cpu_percent:.1f}"
                
            # Обрабатываем None в memory
            memory_display = "N/A"
            if process.memory is not None:
                memory_mb = process.memory.rss / 1024 / 1024
                memory_display = f"{memory_mb:.1f}MB"
            
            print(f"{process.pid:<8} {process.name:<30} {process.ppid:<8} "
                  f"{process.username:<20} {cpu_display:<6} {memory_display:<12} "
                  f"{process.status:<20} {access_icon:<6} {process.formatted_create_time:<10}")
            
    def display_count(self, processes, accessible_processes):
        print(f'Общее количество процессов: {len(processes)}')
        print(f'Количество доступных процессов: {len(accessible_processes)}')
        print(f'Количество НЕдоступных процессов: {len(processes) - len(accessible_processes)}')
        
                
    