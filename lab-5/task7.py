import concurrent.futures
import time
import random

def process_data(item):
    """
    Обрабатывает элемент данных (имитация CPU-bound операции)
    """
    process_time = random.uniform(0.5, 2.0)
    time.sleep(process_time)
    result = item * 2  # Простая операция преобразования
    print(f"Обработан элемент {item} -> {result} (время: {process_time:.2f}с)")
    return result

def task7_thread_pool():
    """
    Задача: Реализуйте обработку данных с использованием пула потоков.
    
    Данные для обработки: список чисел от 1 до 10
    
    Требуется:
    - Обработать все данные с использованием ThreadPoolExecutor
    - Использовать разные размеры пула (2, 4, 8 потоков)
    - Сравнить время выполнения для разных размеров пула
    - Собрать и вывести результаты обработки
    """
    data = list(range(1, 11))
    
    print("=== ОБРАБОТКА ДАННЫХ С ПОМОЩЬЮ ПУЛА ПОТОКОВ ===")
    
    pool_sizes = [2, 4, 8]
    results = {}
    
    for pool_size in pool_sizes:
        print(f"\n--- Пул из {pool_size} потоков ---")
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=pool_size) as executor:
            # Сохраняем порядок с помощью map()
            processed = list(executor.map(process_data, data))
        
        end_time = time.time()
        elapsed = end_time - start_time
        results[pool_size] = elapsed
        print(f"Результаты: {processed}")
    
    print("\n=== СРАВНЕНИЕ ПРОИЗВОДИТЕЛЬНОСТИ ===")
    for pool_size, elapsed in results.items():
        print(f"Пул {pool_size} потоков: {elapsed:.2f} сек")

task7_thread_pool()