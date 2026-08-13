import logging
import pathlib

def setup_custom_logger(name, file_name, log_level='DEBUG', file_mode='a'):
    """
    Создает и настраивает кастомный логгер
    
    Args:
        name: имя логгера
        file_name: имя файла для логов
        log_level: уровень логирования ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
        file_mode: режим работы с файлом ('a' -добавить, 'w' - перезапись)
    """
    logger = logging.getLogger(name)
    # Если логгер уже настроен - возвращаем существующий
    if logger.handlers:
        return logger
    # Преобразуем строковый уровень в числовой
    level = getattr(logging, log_level.upper())
    logger.setLevel(level)
    # Создаем обработчик файла
    log_file = pathlib.Path(__file__).parent.joinpath(file_name)
    file_handler = logging.FileHandler(log_file, mode=file_mode)
    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)-20s, %(name)-15s, %(levelname)-10s, %(message)s'
    )
    file_handler.setFormatter(formatter)
    # Добавляем обработчик к логгеру
    logger.addHandler(file_handler)
    print(f"✅ Логгер '{name}' настроен: файл={file_name}, уровень={log_level}")
    print(f"   Обработчиков: {len(logger.handlers)}")
    return logger

def log_parameters(logger, file_name='tt.log', log_level='DEBUG'):
    def decorator(func):
        def wrapper (*args, **kwargs):
            # Проверяем, настроен ли логгер, если нет - настраиваем
            if not logger.handlers:
                print(f"🔄 Настраиваем логгер '{logger.name}'...")
                setup_custom_logger(
                    name=logger.name or 'default_logger',
                    file_name=file_name,
                    log_level=log_level
                )
            else:
                print(f"✅ Логгер '{logger.name}' уже настроен")
        
            print(f'{file_name=}, {log_level=}, {logger=}')
            logger.info(f"Func {func.__name__} started with args: {args}, kwargs: {kwargs}")
            result = func(*args, **kwargs)
            logger.info(f"Func {func.__name__} finished with result: {result}")
            return result
        return wrapper
    return decorator



#v1 - создаём логгер тут, а настраиваем в декораторе
my_logger = logging.getLogger('my_app')
@log_parameters(my_logger, 'tt.log', "DEBUG")
def calc(a,b,**kwargs):
    return(a+b), kwargs

calc(1,1)
calc(1,2, f=5)



# v2 - Сначала настраиваем логгер, потом используем
my_logger2 = setup_custom_logger(
    name='my_app2', 
    file_name='tt.log', 
    log_level='DEBUG'
)

@log_parameters(my_logger2)
def calc2(a,b,**kwargs):
    return(a+b), kwargs

calc2(34,9)
calc2(3,6, f=7)

def get_all_loggers():
    """Возвращает список всех зарегистрированных логгеров"""
    return list(logging.Logger.manager.loggerDict.keys())

loggers = get_all_loggers()
print("Все логгеры в проекте:")
for logger_name in sorted(loggers):
    print(f"  - {logger_name}")