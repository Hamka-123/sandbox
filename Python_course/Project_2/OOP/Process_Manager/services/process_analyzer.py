#Business Logic / Services

class ProcessAnalyzer:
    
    def sort_by_cpu(self, processes):
        """Сортировка по CPU, игнорируя None значения"""
        # Фильтруем процессы с None в cpu_percent
        valid_processes = [p for p in processes if p.cpu_percent is not None]
        
        # Сортируем только валидные процессы
        return sorted(valid_processes, key=lambda x: x.cpu_percent, reverse=True)
    
    def sort_by_memory(self, processes):
        """Сортировка по памяти"""
        valid_processes = [p for p in processes if p.memory is not None]
        return sorted(valid_processes, 
                     key=lambda x: x.memory.rss if x.memory else 0, 
                     reverse=True)
    
    def find_by_name(self, processes, name):
        """Поиск по имени"""
        return [p for p in processes if name.lower() in p.name.lower()]