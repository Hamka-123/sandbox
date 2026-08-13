import pathlib
import datetime

class MyLogger:
    def __init__(self, filename):
        # Автоматически создаем полный путь к лог-файлу
        self.filename = pathlib.Path(__file__).parent / filename

    def log(self, message):
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.filename, 'a', encoding='utf-8') as file:
            file.write(f'{timestamp} - {message}\n')

    def info(self, message):
        self.log(f'INFO: {message}')

    def warning(self, message):
        self.log(f'WARNING: {message}')

    def error(self, message):
        self.log(f'ERROR: {message}')