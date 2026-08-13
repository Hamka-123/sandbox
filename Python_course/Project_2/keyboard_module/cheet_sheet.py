import keyboard
import time

"""
=== KEYBOARD LIBRARY ШПАРГАЛКА ===

ОСНОВНЫЕ ФУНКЦИИ:
"""

# 1. ПРОВЕРКА НАЖАТИЯ КЛАВИШИ (НЕБЛОКИРУЮЩАЯ)
def check_is_pressed():
    """
    keyboard.is_pressed(key) -> bool
    Проверяет нажата ли клавиша в данный момент
    """
    if keyboard.is_pressed('a'):
        print("Клавиша A нажата")
    if keyboard.is_pressed('ctrl+c'):  # Комбинация
        print("Ctrl+C нажато")

# 2. ЧТЕНИЕ ОДНОЙ КЛАВИШИ (БЛОКИРУЮЩЕЕ)
def read_key_example():
    """
    keyboard.read_key() -> str
    Блокирует выполнение пока не будет нажата любая клавиша
    Возвращает имя клавиши
    """
    key = keyboard.read_key()
    print(f"Вы нажали: {key}")

# 3. ЧТЕНИЕ КЛАВИШИ С ТАЙМАУТОМ
def read_key_timeout():
    """
    keyboard.read_key(timeout=5) -> str или None
    Ждет нажатия клавиши не более timeout секунд
    """
    key = keyboard.read_key(timeout=5)
    if key:
        print(f"Нажато: {key}")
    else:
        print("Время вышло!")

# 4. ОЖИДАНИЕ КОНКРЕТНОЙ КЛАВИШИ
def wait_example():
    """
    keyboard.wait(key) -> None
    Блокирует выполнение пока не будет нажата указанная клавиша
    """
    print("Нажмите ESC для продолжения...")
    keyboard.wait('esc')
    print("Продолжаем!")

# 5. РЕГИСТРАЦИЯ ГОРЯЧИХ КЛАВИШ
def hotkey_example():
    """
    keyboard.add_hotkey(hotkey, callback)
    Регистрирует функцию для вызова при нажатии комбинации
    """
    def say_hello():
        print("Привет!")
    
    def exit_program():
        print("Выход...")
        raise SystemExit
    
    # Регистрируем горячие клавиши
    keyboard.add_hotkey('ctrl+h', say_hello)
    keyboard.add_hotkey('ctrl+q', exit_program)
    
    print("Нажмите Ctrl+H для приветствия или Ctrl+Q для выхода")
    keyboard.wait()  # Бесконечное ожидание

# 6. ОТПРАВКА НАЖАТИЙ КЛАВИШ
def send_keys_example():
    """
    keyboard.send(), keyboard.write() - эмуляция ввода
    """
    time.sleep(2)  # Даем время перейти в текстовый редактор
    
    # Отправить комбинацию клавиш
    keyboard.send('ctrl+a')  # Выделить все
    
    # Напечатать текст
    keyboard.write("Hello World!")
    
    # Отправить одиночную клавишу
    keyboard.send('enter')

# 7. РАБОТА С СОБЫТИЯМИ
def events_example():
    """
    keyboard.read_event() - чтение raw событий
    """
    print("Нажимайте клавиши (ESC для выхода):")
    
    while True:
        event = keyboard.read_event()
        
        print(f"Событие: {event.name} | Тип: {event.event_type} | Scan code: {event.scan_code}")
        
        if event.name == 'esc' and event.event_type == 'down':
            break

"""
=== СПИСОК ПОПУЛЯРНЫХ ИМЕН КЛАВИШ ===

БУКВЫ И ЦИФРЫ:          СПЕЦИАЛЬНЫЕ КЛАВИШИ:
'a', 'b', 'c'...        'space', 'enter', 'esc', 'tab'
'1', '2', '3'...        'backspace', 'delete', 'insert'
                        'home', 'end', 'page up', 'page down'

МОДИФИКАТОРЫ:           СТРЕЛКИ:
'ctrl', 'shift', 'alt'  'up', 'down', 'left', 'right'
'right ctrl', 'right shift'

ФУНКЦИОНАЛЬНЫЕ:         КЛАВИШИ WINDOWS:
'f1', 'f2'...'f12'      'windows', 'right windows'
"""

"""
=== КОМБИНАЦИИ КЛАВИШ ===
Формат: 'modifier+key'
Примеры:
'ctrl+c', 'alt+tab', 'shift+a', 'ctrl+alt+delete'
"""

"""
=== ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===
"""

def game_controls():
    """Пример управления в игре"""
    while True:
        if keyboard.is_pressed('w'):
            print("Движение вперед")
        if keyboard.is_pressed('a'):
            print("Движение влево") 
        if keyboard.is_pressed('s'):
            print("Движение назад")
        if keyboard.is_pressed('d'):
            print("Движение вправо")
        if keyboard.is_pressed('space'):
            print("Прыжок!")
        if keyboard.is_pressed('esc'):
            break
        
        time.sleep(0.1)

def macro_example():
    """Пример макроса"""
    def insert_signature():
        keyboard.write("\n\nС уважением,\nИван Иванов")
    
    # Назначить на Ctrl+Shift+S
    keyboard.add_hotkey('ctrl+shift+s', insert_signature)
    print("Нажмите Ctrl+Shift+S для вставки подписи")
    keyboard.wait('esc')

def non_blocking_listener():
    """Неблокирующий слушатель клавиш"""
    print("Нажимайте клавиши (ESC для выхода)...")
    
    try:
        while True:
            # Проверяем клавиши без блокировки
            if keyboard.is_pressed('esc'):
                print("Выход...")
                break
            elif keyboard.is_pressed('space'):
                print("SPACE нажата")
                time.sleep(0.3)  # Защита от двойного срабатывания
            
            time.sleep(0.01)  # Короткая пауза
            
    except KeyboardInterrupt:
        print("\nПрервано пользователем")

"""
=== ВАЖНЫЕ ЗАМЕЧАНИЯ ===

1. На macOS требует прав администратора
2. is_pressed() работает глобально - даже когда окно не в фокусе
3. Для защиты от двойных срабатываний используйте time.sleep()
4. read_key() и wait() блокируют выполнение программы
5. add_hotkey() работает в фоне, не блокируя основной поток
"""

if __name__ == "__main__":
    # Раскомментируйте для тестирования:
    # check_is_pressed()
    # read_key_example() 
    # hotkey_example()
    non_blocking_listener()