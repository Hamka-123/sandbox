'''
custom class timer:

- thread 1 -> print timer seconds, menu options: start, reset, stop, pause, ...
- thread 2 -> control thread: scan console key, execute menu tasks 

'''
import threading
import keyboard
import time

class MyTimer:
    def __init__(self):
        self.timer_thread = None
        self.timer_running = False
        self.timer_paused = False
        self.current_seconds = 0
        self.duration = 0
        self.status = None
        self.menu = """Нажимайте клавиши:
              CTRL+Z - для выхода из программы
              SHIFT+ENTER - для запуска таймера на 5 сек
              ESC - для остановки таймера
              BACKSPACE - чтобы сбросить счётчик текущего таймера
              SPACE - чтобы поставить на паузу текущий таймер
              F1 - для получения информации о текущем потоке
              """
        
        #запускаем слушателя с управляющим меню
        thread = threading.Thread(target=self.non_blocking_listener)
        thread.start()
    
    # 1. РАБОЧИЙ ПОТОК ТАЙМЕРА
    def timer_worker(self, duration):
        """
        - thread 1 -> print timer seconds, menu options: start, reset, stop, pause, ...
        """
        self.timer_running = True
        self.timer_paused = False
        self.current_seconds = 0
        self.duration = duration
        
        print(f"🚀 Таймер запущен на {self.duration} секунд")
        while self.current_seconds < self.duration and self.timer_running:
            if not self.timer_paused:
                self.current_seconds += 1
                print(f"Timer seconds: {self.current_seconds} / {self.duration}")
            time.sleep(1)
            
        self.timer_running = False
        self.status = "Finished ✅"
        print(self.status)


    # Создание потока
    def start_timer(self, worker, duration, daemon = False):
        self.timer_thread = threading.Thread(target=worker, args=(duration,),daemon = daemon)
        self.timer_thread.start()
        self.status = "running" if self.timer_running == True else "resumed"
        print(f"Timer {self.status}")
        
    def get_duration_from_user(self):
        while True:
            try:
                user_input = input("Сколько секунд ждём? ")
                if user_input.strip() == "":
                    return 5  # Значение по умолчанию
                duration = int(user_input)
                if duration > 0:
                    return duration
                else:
                    print("❌ Введите положительное число")
            except ValueError:
                print("❌ Ошибка! Введите число. Попробуйте снова.")
        
    def stop_timer(self):
        self.timer_thread = None
        self.timer_running = False
        self.timer_paused = False
        self.current_seconds = 0
        self.duration = 0
        self.status = "stoped" if self.timer_running == False else "resumed"
        print(f"Timer {self.status}")
    
    def pause_timer(self):
        self.timer_paused = not self.timer_paused
        self.status = "paused" if self.timer_paused else "resumed"
        print(f"Timer {self.status}")
    
    def reset_timer(self):
        self.timer_running = True
        self.timer_paused = False
        self.current_seconds = 0
        self.status = "reseted" if self.current_seconds == 0 else "resumed"
        print(f"Timer {self.status}")
    
    def print_timer_info(self):
        print(f"Running: {self.timer_running}, Paused: {self.timer_paused}, Seconds: {self.current_seconds}/{self.duration}")
    
    # 2. СЛУШАТЕЛЬ НАЖАТИЯ КЛАВИШ
    def non_blocking_listener(self):
        """Неблокирующий слушатель клавиш
        - thread 2 -> control thread: scan console key, execute menu tasks
        """
        print(self.menu)
        try:
            while True:
                # Проверяем клавиши без блокировки
                if keyboard.is_pressed('ctrl') and keyboard.is_pressed('z'):
                    print("Exit...")
                    break
                elif keyboard.is_pressed('shift') and keyboard.is_pressed('enter'):
                    print("start...")
                    # Запускаем input в отдельном потоке
                    def ask_duration_and_start(): #TODO - разобраться с запросом данных от юзера
                        duration = self.get_duration_from_user()
                        if duration > 0:
                            self.start_timer(self.timer_worker, duration)
                    
                    threading.Thread(target=ask_duration_and_start).start()
                    time.sleep(0.3) 
                elif keyboard.is_pressed('esc'):
                    print("stoped...")
                    self.stop_timer()
                    print(self.menu)
                    time.sleep(0.3)  
                elif keyboard.is_pressed('backspace'):
                    print("reset...")
                    self.reset_timer()
                    time.sleep(0.3)  
                elif keyboard.is_pressed('space'):
                    print("pause...")
                    self.pause_timer()
                    time.sleep(0.3)  
                elif keyboard.is_pressed('f1'):
                    print("print info...")
                    self.print_timer_info()
                    time.sleep(0.3)
                
                time.sleep(0.01)  # Короткая пауза
                
        except KeyboardInterrupt:
            print("\nПрервано пользователем")


        
timer1 = MyTimer()