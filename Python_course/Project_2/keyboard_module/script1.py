import keyboard
import time


'''
print("Press ESC to stop...")
while True:
    if keyboard.is_pressed('esc'):  # 'esc' в нижнем регистре
        print('Stop')
        break
    time.sleep(0.1)  # Небольшая задержка чтобы не грузить CPU
'''
    
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
        
events_example()