# Start multiple threads
# Start separate thread: monitor
# monitor, once a second, print aal threads status

import os
import random
import threading
import time

# Глобальный список для хранения информации о всех потоках
all_threads_info = []

print(f"{threading.current_thread().is_alive()=}")

class MyThread(threading.Thread):
    def __init__(self, thread_id, delay):
        super().__init__()
        self.thread_id = thread_id
        self.delay = delay

        # Добавляем информацию о потоке в глобальный список
        all_threads_info.append({
            'name': self.name,
            'thread': self,
            'created_time': time.time()
        })
        
    def run(self):
        """Метод run автоматически выполняется при start()"""
        print(f"Поток {self.thread_id} начал работу")
        time.sleep(self.delay)
        print(f"Поток {self.thread_id} завершил работу после {self.delay:.2f} сек")

# Добавляем главный поток (main) в мониторинг ДО создания других потоков
main_thread = threading.current_thread()
all_threads_info.append({
    'name': 'Main',
    'thread': main_thread,
    'created_time': time.time(),
})
# Использование
threads = []
for i in range(5):
    t = MyThread(thread_id=i, delay=random.uniform(1, 3))
    threads.append(t)
    t.start()

def monitoring():
    # Добавляем сам мониторинг-поток в список
    monitor_thread = threading.current_thread()
    all_threads_info.append({
        'name': 'Monitor',
        'thread': monitor_thread,
        'created_time': time.time(),
    })
    while True:
        #os.system('clear')  
        print(f"===== Total threads: {len(all_threads_info)} =====")
        print(f"===== Active threads: {threading.active_count()} =====")
        
        # ВЫВОДИМ ИМЕНА В СТРОКУ (из нашего глобального списка)
        print("Thread names:", " ".join(f"{info['name']:^10}" for info in all_threads_info))
        
        # ВЫВОДИМ СТАТУСЫ В СТРОКУ ПОД ИМЕНАМИ
        status_line = []
        for info in all_threads_info:
            thr = info['thread']
            if thr.is_alive():
                status_line.append(f"{'✅':^10}")
            else:
                status_line.append(f"{'❌':^10}")
        
        print("Status:     ", " ".join(status_line))
        
        # Дополнительная информация о времени создания
        time_line = []
        for info in all_threads_info:
            created_str = time.strftime('%H:%M:%S', time.localtime(info['created_time']))
            time_line.append(f"{created_str:^10}")
        
        print("Created:    ", " ".join(time_line))
        
        time.sleep(1)

monitor = threading.Thread(target=monitoring, daemon=True)
monitor.start()

# Ждем завершения всех рабочих потоков
for t in threads:
    t.join()

print("All worker threads finished!")

# Даем посмотреть на результат 5 секунд
time.sleep(5)