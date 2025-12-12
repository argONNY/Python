import time
import threading
import multiprocessing
import asyncio
import requests

def io_task(name, duration):
    """I/O-bound задача (имитация)"""
    time.sleep(duration)
    return f"{name} completed"

async def async_io_task(name, duration):
    """Асинхронная I/O-bound задача"""
    await asyncio.sleep(duration)
    return f"{name} completed"

def run_io_task_sync(task):
    """Обёртка для синхронного вызова"""
    name, duration = task
    return io_task(name, duration)

def run_io_task_thread(task):
    """Обёртка для потоков"""
    name, duration = task
    return io_task(name, duration)

def run_io_task_process(task):
    """Обёртка для процессов"""
    name, duration = task
    return io_task(name, duration)

async def run_async_task(task):
    """Обёртка для асинхронного выполнения"""
    name, duration = task
    return await async_io_task(name, duration)

def task5_performance_comparison():
    """
    Задача: Сравните производительность разных подходов.
    
    Набор I/O-bound задач (имитация):
    1. "Task1" - 2 секунды
    2. "Task2" - 3 секунды
    3. "Task3" - 1 секунда
    4. "Task4" - 2 секунды
    5. "Task5" - 1 секунда
    
    Требуется:
    - Реализовать выполнение одним потоком
    - Реализовать выполнение несколькими потоками  
    - Реализовать выполнение несколькими процессами
    - Реализовать асинхронное выполнение
    - Сравнить время выполнения каждого подхода
    - Сделать выводы о эффективности
    """
    tasks = [("Task1", 2), ("Task2", 3), ("Task3", 1), ("Task4", 2), ("Task5", 1)]
    
    # === 1. Синхронное выполнение (один поток) ===
    print("=== СИНХРОННОЕ ВЫПОЛНЕНИЕ ===")
    start = time.time()
    sync_results = [run_io_task_sync(task) for task in tasks]
    sync_time = time.time() - start
    print(f"Результаты: {sync_results}")

    # === 2. Многопоточное выполнение ===
    print("\n=== МНОГОПОТОЧНОЕ ВЫПОЛНЕНИЕ ===")
    start = time.time()
    threads = []
    results = [None] * len(tasks)
    
    def worker(idx, task):
        results[idx] = run_io_task_thread(task)
    
    for i, task in enumerate(tasks):
        thread = threading.Thread(target=worker, args=(i, task))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    thread_time = time.time() - start
    print(f"Результаты: {results}")

    # === 3. Многопроцессное выполнение ===
    print("\n=== МНОГОПРОЦЕССНОЕ ВЫПОЛНЕНИЕ ===")
    start = time.time()
    with multiprocessing.Pool(processes=len(tasks)) as pool:
        process_results = pool.map(run_io_task_process, tasks)
    process_time = time.time() - start
    print(f"Результаты: {process_results}")

    # === 4. Асинхронное выполнение ===
    print("\n=== АСИНХРОННОЕ ВЫПОЛНЕНИЕ ===")
    async def run_async():
        tasks_async = [run_async_task(task) for task in tasks]
        return await asyncio.gather(*tasks_async)
    
    start = time.time()
    async_results = asyncio.run(run_async())
    async_time = time.time() - start
    print(f"Результаты: {async_results}")

    # === ВЫВОД РЕЗУЛЬТАТОВ ===
    print("\n=== АНАЛИЗ РЕЗУЛЬТАТОВ ===")
    print(f"Синхронное время: {sync_time:.2f} сек")
    print(f"Многопоточное время: {thread_time:.2f} сек") 
    print(f"Многопроцессное время: {process_time:.2f} сек")
    print(f"Асинхронное время: {async_time:.2f} сек")
    
    # === ВЫВОДЫ ===
    print("\n=== ВЫВОДЫ ===")
    print("Для I/O-bound задач синхронное выполнение самое медленное")
    print("Многопоточность и асинхронность дают почти одинаковый результат")
    print("Асинхронность наиболее эффективна по ресурсам (один поток, нет переключения контекста)")
    print("Многопроцессность избыточна для I/O-bound задач (накладные расходы на IPC)")
    print("\nНаилучший выбор для I/O-bound задач: асинхронное программирование")

# Запуск задачи
if __name__ == "__main__":
    task5_performance_comparison()