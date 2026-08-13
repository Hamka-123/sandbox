#Domain / Model

from datetime import datetime
from typing import Optional


class ProcessEntity:
    
    def __init__(self, pid, name, status, ppid, username, cpu_percent, memory, create_time, accessible=True):
        self.pid:int = pid
        self.name:str = name
        self.status:str = status
        self.ppid = ppid
        self.username:str = username
        self.cpu_percent:float = cpu_percent
        self.memory:object = memory
        self.create_time:Optional[float] = create_time
        self.accessible = accessible
    
    @property
    def formatted_create_time(self) -> str:
        if self.create_time:
            return datetime.fromtimestamp(self.create_time).strftime('%H:%M:%S')
        return "N/A"
    
    def __repr__(self):
        access_indicator = "🔒" if not self.accessible else "✅"
        mem_mb = self.memory.rss / 1024 / 1024 if self.memory else 0
        cpu = self.cpu_percent if self.cpu_percent is not None else 0
        return f"{access_indicator} {self.pid} {self.name} {self.status} {self.ppid} {self.username}({cpu:.1f}% CPU, {mem_mb:.1f} MB RAM {self.formatted_create_time})"
    