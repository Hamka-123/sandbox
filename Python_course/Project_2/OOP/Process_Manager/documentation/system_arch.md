https://psutil.readthedocs.io/en/latest/

OOP/Process_Manager/documentation/acrh.puml
OOP/Process_Manager/documentation/process_lifecycle.puml
          ┌───────────────────────────┐
          │       User / CLI          │
          │       (ProcessView)       │
          └───────────┬────────────-──┘
                      │
                      ▼
          ┌────────────────────────-───┐
          │  Application Layer / Facade│
          │       ProcessManager       │
          │----------------------------│
          │ - get_process_list()       │
          │ - kill_process(pid)        │
          │ - pause_process(pid)       │
          │ - analyze_processes()      │
          └───────────┬────────────--──┘
                      │
        ┌─────────────┼──────────────┐
        ▼             ▼              ▼
 ┌────────────---─┐ ┌─────────----────┐ ┌────────────----─┐
 │ ProcessMonitor │ │ ProcessAnalyzer │ │ ProcessOperator │
 │  Business Logic│ │  Business Logic │ │  Business Logic │
 │ - update_list()│ │ - filter()      │ │ - kill()        │
 │ - get_current()│ │ - sort()        │ │ - pause()       │
 └─────┬───────-──┘ └─────┬──────--───┘ └─────┬────────--─┘
       │                 │                 │
       ▼                 ▼                 ▼
 ┌───────────────────────────-────┐
 │       Data Access Layer        │
 │--------------------------------│
 │ ProcessRepository              │ ← работа с psutil
 │  - fetch_all_processes()       │
 │  - get_process_by_pid()        │
 │ TestProcessFactory             │ ← безопасные тестовые процессы
 │  - create_test_process()       │
 │  - terminate_test_process()    │
 └─────────────┬─────────────────┘
               │
               ▼
        ┌───────────────┐
        │ ProcessEntity │
        │ (Domain Model)│
        │ PID, name,    │
        │ CPU, memory,  │
        │ status        │
        └───────────────┘

Process_Manager/
│
├─ domain/
│   └─ process_entity.py # Сущность процесса сквозная
│
├─ application/
│   └─ process_manager.py # Фасад/менеджер
│
├─ presentation/
│   └─ process_view.py # Представление (CLI)
│
├─ services/
│   ├─ process_monitor.py # Мониторинг
│   ├─ process_analyzer.py # Анализ (поиск, сортировка)
│   └─ process_operator.py # Операции (kill, pause)
│
├─ data_access/
│   ├─ process_repository.py # Работа с psutil 
│   └─ test_process_factory.py # создаёт безопасные тестовые процессы
│
└─ main.py              # точка входа


'''
Текущие проблемы:
* Архитектура: чистая многослойная - может избыточная для такой задачи, но хотелось сделать аналог htop (real-time)
1) Большое кол-во процессов (522, 149 из них AccessDenied) + количество полей 9 - долго - одна большая доменная модель
2) В каждом методе менеджера заново получаю процессы
3) Не реализованы тестовые процессы для безопасной проверки kill
4) Мониторинг не реализован
5) CPU и Memory - нужно замерять, дополнительное время

Варианты решения:
1) Получать один раз и делать снепшоты, работать с ними (передавать список объектов из метода в метод)
2) Создать авто-обновляемый репозиторий
3) Разбить доменную модель на части и дополнять остальные данные по мере необходимости
4) Добавить кеширование

