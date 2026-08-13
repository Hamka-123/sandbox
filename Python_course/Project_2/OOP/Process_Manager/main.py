# main.py
from datetime import time
import time
from application.process_manager import ProcessManager

def main():
    manager = ProcessManager()
    
    print("=== Process Manager ===")
    start = time.perf_counter()
    # 1. Показать процессы
    print("\n--- Processes ---")
    manager.display_processes()
    finish = time.perf_counter()
    execution_time = finish - start
    print(f"\n=== Execution Time: {execution_time:.3f} seconds ===")
    
    # 2. Найти Python процессы
    print("\n--- Python processes ---")
    python_processes = manager.find_processes_by_name("python")
    manager.view.display_processes(python_processes[:5])
    
    # 3. Топ по CPU
    print("\n--- Top 5 CPU processes ---")
    top_cpu = manager.get_top_cpu_processes(5)
    manager.view.display_processes(top_cpu)
    
    # 4. Мониторинг 
    print("\n--- Starting monitor ---")
    manager.start_monitoring(10)
    
if __name__ == "__main__":
    main()