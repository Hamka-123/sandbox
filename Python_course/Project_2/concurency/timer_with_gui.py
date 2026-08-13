import tkinter as tk
from tkinter import ttk
import threading
import time

class TimerApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎯 Таймеры")
        self.root.geometry("400x300")
        self.root.configure(bg='white')
        
        # Переменные для хранения значений таймеров
        self.times = [0, 0, 0]
        self.delays = [1, 2, 5]  # Задержки в секундах
        
        self.setup_ui()
        self.start_timers()
    
    def setup_ui(self):
        # Заголовок
        title_label = tk.Label(
            self.root, 
            text="🎯 СИСТЕМА ТАЙМЕРОВ", 
            font=("Helvetica", 18, "bold"),
            bg='white',
            fg='navy'
        )
        title_label.pack(pady=20)
        
        # Разделитель
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(fill='x', padx=50, pady=10)
        
        # Фрейм для таймеров
        timer_frame = tk.Frame(self.root, bg='white')
        timer_frame.pack(pady=20)
        
        # Создаем виджеты для каждого таймера
        self.timer_labels = []
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Красный, бирюзовый, синий
        
        for i in range(3):
            # Фрейм для одного таймера
            frame = tk.Frame(timer_frame, bg='white', relief='ridge', bd=2)
            frame.pack(pady=8, padx=20, fill='x')
            
            # Название таймера
            name_label = tk.Label(
                frame,
                text=f"Таймер {i+1} ({self.delays[i]} сек):",
                font=("Helvetica", 12, "bold"),
                bg='white',
                fg='#333'
            )
            name_label.pack(side=tk.LEFT, padx=10, pady=8)
            
            # Значение таймера
            value_label = tk.Label(
                frame,
                text="0",
                font=("Helvetica", 16, "bold"),
                fg=colors[i],
                bg='white',
                width=6
            )
            value_label.pack(side=tk.RIGHT, padx=10, pady=8)
            self.timer_labels.append(value_label)
        
        # Фрейм для кнопок
        button_frame = tk.Frame(self.root, bg='white')
        button_frame.pack(pady=30)
        
        # Кнопка сброса
        reset_btn = tk.Button(
            button_frame,
            text="🔄 Сбросить все",
            command=self.reset_timers,
            font=("Helvetica", 12),
            bg='#FFE66D',
            fg='black',
            relief='raised',
            bd=3,
            padx=20,
            pady=8
        )
        reset_btn.pack(side=tk.LEFT, padx=10)
        
        # Кнопка выхода
        exit_btn = tk.Button(
            button_frame,
            text="❌ Выход",
            command=self.root.quit,
            font=("Helvetica", 12),
            bg='#FF6B6B',
            fg='white',
            relief='raised',
            bd=3,
            padx=20,
            pady=8
        )
        exit_btn.pack(side=tk.LEFT, padx=10)
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("🟢 Таймеры активны")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Helvetica", 10),
            bg='lightgray',
            relief='sunken',
            bd=1
        )
        status_bar.pack(side=tk.BOTTOM, fill='x')
    
    def reset_timers(self):
        """Сброс всех таймеров"""
        self.times = [0, 0, 0]
        for i in range(3):
            self.timer_labels[i].config(text="0")
        self.status_var.set("🔄 Таймеры сброшены")
        # Через 2 секунды вернем обычный статус
        self.root.after(2000, lambda: self.status_var.set("🟢 Таймеры активны"))
    
    def update_ui(self):
        """Обновление интерфейса"""
        for i in range(3):
            self.timer_labels[i].config(text=str(self.times[i]))
        
        # Планируем следующее обновление через 100мс
        self.root.after(100, self.update_ui)
    
    def start_timers(self):
        """Запуск таймеров в отдельных потоках"""
        def worker_timer(delay, timer_num):
            while True:
                time.sleep(delay)
                self.times[timer_num] += 1
        
        # Запускаем потоки для каждого таймера
        for i, delay in enumerate(self.delays):
            thread = threading.Thread(
                target=worker_timer, 
                args=(delay, i), 
                daemon=True
            )
            thread.start()
        
        # Запускаем обновление интерфейса
        self.update_ui()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    app = TimerApp()
    app.run()