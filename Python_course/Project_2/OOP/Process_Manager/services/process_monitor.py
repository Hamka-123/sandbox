#Business Logic / Services

class ProcessMonitor:
    
    def __init__(self, repository=None):
        self.repository = repository
    
    def watch_processes(self, interval=2, duration=30):
        """Мониторинг процессов"""
        if not self.repository:
            print("❌ Repository not available for monitoring")
            return
        print(f"🔍 Monitoring processes for {duration} seconds...")