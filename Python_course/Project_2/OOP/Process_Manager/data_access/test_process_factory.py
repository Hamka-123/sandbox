#Data Access / Repository / Test Factory
#Тестовые процессы → TestProcessFactory

import psutil
from domain.process_entity import ProcessEntity

class TestProcessFactory:
    """
    Класс создания и доступа к тестовым процессам системы через psutil.
    Преобразует каждый процесс в объект ProcessEntity.
    """
    
    def __init__(self):
        pass