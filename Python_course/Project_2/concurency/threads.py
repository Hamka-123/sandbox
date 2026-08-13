# Start simple thread
'''
import threading
import time

START_TIME = time.perf_counter_ns()
THREADS = 10

def worker():
    print(f"{time.perf_counter_ns() - START_TIME} {threading.current_thread().name}")
    pass

print(f"{time.perf_counter_ns() - START_TIME} {threading.current_thread().name}")

threading.Thread(
    target=lambda: print(f"{time.perf_counter_ns() - START_TIME} {threading.current_thread().name}")
    ).start()

threading.Thread(target=worker).start()

threads = [threading.Thread(target=worker) for _ in range(THREADS)]
for t in threads: t.start()


'''
# Start multiple threads
import random,threading,time

START_TIME = time.perf_counter_ns()
THREADS = 10
print(f"{time.perf_counter_ns() - START_TIME:15} {threading.current_thread().name} STARTED")

def worker():
    print(f"{time.perf_counter_ns() - START_TIME:15} {threading.current_thread().name} STARTED")
    time.sleep(random.randint(1, 100) // 10) # Thread job simulate
    print(f"{time.perf_counter_ns() - START_TIME:15} {threading.current_thread().name} STOPPED")    
    pass
print(f"{time.perf_counter_ns() - START_TIME:15} {threading.current_thread().name} Creating threads")
threads = [threading.Thread(target=worker) for _ in range(THREADS)]
print(f"{time.perf_counter_ns() - START_TIME:15} {threading.current_thread().name} Starting threads")
for t in threads: t.start()
print(f"{time.perf_counter_ns() - START_TIME:15} {threading.current_thread().name} STOPPED")

"""
BASIC THREADING CHEATSHEET
Импорт и базовое использование
"""
import threading
import time
import random


# 1. СОЗДАНИЕ И ЗАПУСК ПОТОКА
def simple_worker(message):
    """Простая функция для выполнения в потоке"""
    print(f"Поток начал работу: {message}")
    time.sleep(2)  # Имитация работы
    print(f"Поток завершил работу: {message}")


# Создание потока
thread = threading.Thread(target=simple_worker, args=("Привет мир!",))
thread.start()  # Запуск потока
thread.join()   # Ожидание завершения потока


print("\n" + "="*50 + "\n")


# 2. КЛАССОВЫЙ ПОДХОД
class MyThread(threading.Thread):
    def __init__(self, thread_id, delay):
        super().__init__()
        self.thread_id = thread_id
        self.delay = delay
    
    def run(self):
        """Метод run автоматически выполняется при start()"""
        print(f"Поток {self.thread_id} начал работу")
        time.sleep(self.delay)
        print(f"Поток {self.thread_id} завершил работу после {self.delay} сек")


# Использование
threads = []
for i in range(3):
    t = MyThread(thread_id=i, delay=random.uniform(1, 3))
    threads.append(t)
    t.start()

# Ожидание завершения всех потоков
for t in threads:
    t.join()


print("\n" + "="*50 + "\n")


# 3. СИНХРОНИЗАЦИЯ - LOCK (БЛОКИРОВКА)
shared_counter = 0
lock = threading.Lock()  # Создание блокировки


def counter_worker():
    """Работа с разделяемым ресурсом с блокировкой"""
    global shared_counter
    
    for _ in range(1000):
        with lock:  # Автоматическое получение и освобождение блокировки
            shared_counter += 1
        # Эквивалент:
        # lock.acquire()
        # try:
        #     shared_counter += 1
        # finally:
        #     lock.release()


# Запуск нескольких потоков для демонстрации
counter_threads = []
for _ in range(5):
    t = threading.Thread(target=counter_worker)
    counter_threads.append(t)
    t.start()

for t in counter_threads:
    t.join()

print(f"Итоговое значение счетчика: {shared_counter} (должно быть 5000)")


print("\n" + "="*50 + "\n")


# 4. SEMAPHORE (СЕМАФОР) - ограничение количества одновременных потоков
semaphore = threading.Semaphore(2)  # Максимум 2 потока одновременно


def limited_worker(worker_id):
    """Работа с ограничением через семафор"""
    with semaphore:
        print(f"Рабочий {worker_id} начал работу")
        time.sleep(2)
        print(f"Рабочий {worker_id} завершил работу")


print("Семафор - только 2 рабочих одновременно:")
workers = []
for i in range(5):
    t = threading.Thread(target=limited_worker, args=(i,))
    workers.append(t)
    t.start()

for t in workers:
    t.join()


print("\n" + "="*50 + "\n")


# 5. EVENT (СОБЫТИЕ) - координация между потоками
event = threading.Event()


def waiter():
    """Поток, ожидающий событие"""
    print("Ожидающий поток: жду сигнала...")
    event.wait()  # Блокировка до установки события
    print("Ожидающий поток: получил сигнал!")


def setter():
    """Поток, устанавливающий событие"""
    time.sleep(2)
    print("Устанавливающий поток: отправляю сигнал!")
    event.set()  # Установка события - разблокировка всех ожидающих


t1 = threading.Thread(target=waiter)
t2 = threading.Thread(target=setter)

t1.start()
t2.start()

t1.join()
t2.join()


print("\n" + "="*50 + "\n")


# 6. CONDITION (УСЛОВИЕ) - сложная синхронизация
condition = threading.Condition()
shared_queue = []
MAX_SIZE = 3


def producer():
    """Производитель - добавляет элементы в очередь"""
    for i in range(10):
        time.sleep(0.1)
        with condition:
            if len(shared_queue) >= MAX_SIZE:
                print("Очередь полна, производитель ждет...")
                condition.wait()  # Ждет, пока consumer не освободит место
            
            item = f"Элемент {i}"
            shared_queue.append(item)
            print(f"Произведен: {item}")
            condition.notify()  # Уведомляет потребителя


def consumer():
    """Потребитель - забирает элементы из очереди"""
    for _ in range(10):
        time.sleep(0.2)
        with condition:
            if not shared_queue:
                print("Очередь пуста, потребитель ждет...")
                condition.wait()  # Ждет, пока producer не добавит элемент
            
            item = shared_queue.pop(0)
            print(f"Потреблен: {item}")
            condition.notify()  # Уведомляет производителя


prod = threading.Thread(target=producer)
cons = threading.Thread(target=consumer)

prod.start()
cons.start()

prod.join()
cons.join()


print("\n" + "="*50 + "\n")


# 7. TIMER (ТАЙМЕР) - выполнение через указанное время
def delayed_task():
    print("Таймер: задача выполнена через 3 секунды!")


timer = threading.Timer(3.0, delayed_task)
timer.start()
# timer.cancel()  # Можно отменить, если нужно


print("\n" + "="*50 + "\n")


# 8. THREAD-LOCAL DATA - локальные данные потока
thread_local = threading.local()


def show_thread_data():
    """Каждый поток имеет свою копию thread-local данных"""
    if not hasattr(thread_local, "data"):
        thread_local.data = f"Данные для {threading.current_thread().name}"
    
    print(f"{threading.current_thread().name}: {thread_local.data}")


# Демонстрация thread-local данных
local_threads = []
for i in range(3):
    t = threading.Thread(
        target=show_thread_data,
        name=f"Thread-{i}"
    )
    local_threads.append(t)
    t.start()

for t in local_threads:
    t.join()


print("\n" + "="*50 + "\n")


# 9. DAEMON THREADS (ДЕМОН-ПОТОКИ)
def daemon_worker():
    """Демон-поток завершается при завершении main-потока"""
    while True:
        print("Демон работает...")
        time.sleep(1)


# Демон-поток (завершится при завершении программы)
daemon_thread = threading.Thread(target=daemon_worker, daemon=True)
daemon_thread.start()

# Главный поток работает 3 секунды, затем программа завершится
# и демон-поток тоже завершится принудительно
time.sleep(3)
print("Главный поток завершается -> демон-поток тоже завершится")


print("\n" + "="*50 + "\n")


# 10. ПОЛЕЗНЫЕ МЕТОДЫ И АТРИБУТЫ
def info_worker():
    """Демонстрация полезных методов"""
    current = threading.current_thread()
    print(f"Имя потока: {current.name}")
    print(f"ID потока: {current.ident}")
    print(f"Жив ли поток: {current.is_alive()}")
    print(f"Демон ли: {current.daemon}")
    
    # Активные потоки
    active_count = threading.active_count()
    print(f"Активных потоков: {active_count}")
    
    # Список всех активных потоков
    # for thread in threading.enumerate():
    #     print(f"  - {thread.name}")


info_thread = threading.Thread(target=info_worker, name="InfoThread")
info_thread.start()
info_thread.join()




# Custom thread class

import threading
from time import sleep


class MyThread(threading.Thread):
    
    def __init__(self, name = None, daemon = None, target:function|None = None, run_parameter:int | None = 0):
        # super().__init__(name=name, daemon=daemon, target=target) 
        super().__init__(name=name, daemon=daemon)
        self.target = target
        self.par1 = run_parameter
        self.__do_stop = False
        pass
    
    def run(self): # Thread task  
            
        print(f"{self.name=}  {self.daemon=} {self.par1=} {self.target=}")
        # if self.target != None: print(self.target)
        if self.target != None: 
            self.target()
        self.__inner_task()
        pass
    
    def stop(self):
        self.__do_stop = True
        pass
    
    def __inner_task(self):
        # TO some additional task 
        while True:
            print("Working ...")
            sleep(0.5)
            if self.__do_stop: break
        
        pass
    
    pass

t1 = MyThread(
    name="MyNewThread", 
    daemon=False, 
    run_parameter=22)
t1.start()
'''
MyThread(
    name="MyNewThread", 
    daemon=False, 
    target=lambda:print('First TARGET FUNCTION CALLED!!'), 
    run_parameter=66).start()


MyThread(
    name="MyNewThread", 
    daemon=False, 
    target=lambda:print('Second TARGET FUNCTION CALLED!!'), 
    run_parameter=55).start()

'''

sleep(5)
t1.stop()