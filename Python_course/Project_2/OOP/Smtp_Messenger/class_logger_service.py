import json
import datetime
import pathlib
import sys
from typing import Any, Dict, Optional

class LoggerService:
    def __init__(self, filename):
        self.filename = pathlib.Path(filename)

    def _log(self, level: str, message: str, analytics_data: Optional[Dict[str, Any]] = None):
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        
        # Добавляем аналитические данные если они есть
        if analytics_data:
            log_entry["analytics"] = analytics_data
        
        try:
            with open(self.filename, 'a', encoding='utf-8') as file:
                json.dump(log_entry, file, ensure_ascii=False)
                file.write('\n')
        except Exception as e:
            print(f"Ошибка записи в лог: {e}")

    def info(self, message: str, analytics_data: Optional[Dict[str, Any]] = None):
        self._log("INFO", message, analytics_data)

    def warning(self, message: str, analytics_data: Optional[Dict[str, Any]] = None):
        self._log("WARNING", message, analytics_data)

    def error(self, message: str, analytics_data: Optional[Dict[str, Any]] = None):
        self._log("ERROR", message, analytics_data)