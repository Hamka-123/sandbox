# producers threads
# consumers threads

import random
import threading
import time
import statistics

 
PRODUCERS = 3
CONSUMERS = 3
QUEUE_CAPACITY = 10
START_TIME = time.perf_counter_ns() // 1_000_000
RED_TEXT = '\u001b[38;2;255;0;0;1m'
GREEN_TEXT = '\u001b[38;2;0;255;0;1m'
RESET_CONSOLE = '\u001b[0m'

queue_empty_event = threading.Event() #очередь пуста
queue_crowded_event = threading.Event() #очередь переполнена

# Изначально очередь пуста, но не переполнена
queue_empty_event.set()    # очередь пуста - ждем
queue_crowded_event.clear()    # можно производить

#QUEUE1_LOCK = threading.Lock()
#QUEUE2_LOCK = threading.Lock()
# Для мониторинга
queue_sizes = []
monitor_running = True

resources_queue = [] # STORE

# resource - timestamp

def producer_worker(delay):
    while True:
        time.sleep(delay) # Travel time 
        
            # Ждем, если очередь переполнена
        if queue_crowded_event.is_set():
            queue_crowded_event.wait()
            
        # Пытаемся добавить элемент
        if len(resources_queue) < QUEUE_CAPACITY:
            new_item = (time.perf_counter_ns() // 1_000_000) - START_TIME
            resources_queue.append(new_item)
            print(f'{threading.current_thread().name}  produced {new_item=}, current queue:\n {resources_queue} ')
            
            # Если была пустая очередь - теперь можно потреблять
            if len(resources_queue) == 1:
                queue_empty_event.clear()
                print(f" - {threading.current_thread().name} Queue has space! Producers can work...")
            
            # Если заполнили очередь - стоп производителям
            if len(resources_queue) >= QUEUE_CAPACITY:
                queue_crowded_event.set()
                print(f" - {threading.current_thread().name} Queue full! Producers waiting...")
        else:
            # На случай race condition
            queue_crowded_event.set()
            

def consumer_worker(delay):
    while True:
        time.sleep(delay) # Create order time 
        # if QUEUE1_LOCK.acquire(3): 
        #     # Try second queue
        #     pass
        
        # Ждем, если очередь пуста
        if queue_empty_event.is_set():
            queue_empty_event.wait()
            
        # Пытаемся забрать элемент
        if len(resources_queue) > 0:
            new_item = resources_queue[0]
            resources_queue.remove(new_item)
            print(f'{threading.current_thread().name}  consumed {new_item=}, current queue:\n {resources_queue} ')
            
            # Если освободили место в очереди - можно производить
            if len(resources_queue) == QUEUE_CAPACITY - 1:
                queue_crowded_event.clear()
                print(f" - {threading.current_thread().name} Queue has space! Producers can work...")
            
            # Если опустошили очередь - стоп потребителям
            if len(resources_queue) == 0:
                queue_empty_event.set()
                print(f" - {threading.current_thread().name} Queue empty! Consumers waiting...")
        else:
            # На случай race condition
            queue_empty_event.set()

def monitor_performance():
    """Мониторинг производительности каждые 3 секунды"""
    while monitor_running:
        time.sleep(8)
        
        # Безопасно получаем размер очереди (может быть немного неточным)
        current_size = len(resources_queue)
        queue_sizes.append(current_size)
        
        # Сохраняем только последние 20 измерений
        if len(queue_sizes) > 20:
            queue_sizes.pop(0)
    
        if queue_sizes:
            try:
                avg_size = statistics.mean(queue_sizes)
                max_size = max(queue_sizes)
                min_size = min(queue_sizes)
                
                print(f"\n{'='*50}")
                print(f"📊 МОНИТОРИНГ ПРОИЗВОДИТЕЛЬНОСТИ")
                print(f"📦 Текущий размер очереди: {current_size}/{QUEUE_CAPACITY}")
                print(f"📈 Средний размер: {avg_size:.1f}")
                print(f"⬆️  Максимальный: {max_size}")
                print(f"⬇️  Минимальный: {min_size}")
                
                # Рекомендации
                if avg_size > QUEUE_CAPACITY * 0.8:
                    print(f"🚨 ВНИМАНИЕ: Очередь почти полная! Добавьте потребителей")
                elif avg_size < QUEUE_CAPACITY * 0.2:
                    print(f"⚠️  Очередь почти пустая! Добавьте производителей")
                else:
                    print(f"✅ Баланс хороший!")
                    
                print(f"{'='*50}\n")
                
            except statistics.StatisticsError:
                # На случай если статистика не может быть вычислена
                pass

producers = [threading.Thread(name= RED_TEXT + f'Producer_{i+1}' + RESET_CONSOLE, target=producer_worker,  kwargs={'delay':random.randint(10,100) // 5}) for i in range(PRODUCERS)]
consumers = [threading.Thread(name= GREEN_TEXT + f'Consumer_{i+1}' + RESET_CONSOLE, target=consumer_worker, kwargs={'delay':random.randint(10,100) // 5})  for i in range(CONSUMERS)]
# Мониторинг потоков
monitor_thread = threading.Thread(target=monitor_performance, name="Monitor")
monitor_thread.daemon = True

for t in producers: t.start()
for t in consumers: t.start()

monitor_thread.start()

