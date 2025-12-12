import asyncio
import time
from datetime import datetime

async def scheduled_task(name, priority, duration, semaphore):
    """
    Задача с приоритетом и временем выполнения
    
    Параметры:
    name (str): название задачи
    priority (int): приоритет (1 - высший)
    duration (float): время выполнения
    semaphore (asyncio.Semaphore): семафор для ограничения параллелизма
    """
    async with semaphore:  # Ограничиваем одновременное выполнение
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Задача '{name}' (приоритет {priority}) начата")
        await asyncio.sleep(duration)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Задача '{name}' завершена")
        return f"Результат {name}"

async def task6_async_scheduler():
    """
    Задача: Создайте асинхронный планировщик задач.
    
    Задачи:
    1. "Экстренная задача" - приоритет 1, длительность 1 сек
    2. "Важная задача" - приоритет 2, длительность 2 сек  
    3. "Обычная задача A" - приоритет 3, длительность 3 сек
    4. "Обычная задача B" - приоритет 3, длительность 2 сек
    5. "Фоновая задача" - приоритет 4, длительность 5 сек
    
    Требуется:
    - Запустить задачи в порядке приоритета
    - Обеспечить выполнение высокоприоритетных задач первыми
    - Реализовать ограничение на одновременное выполнение (не более 2 задач)
    - Вывести порядок завершения задач
    """
    tasks_with_priority = [
        ("Экстренная задача", 1, 1),
        ("Важная задача", 2, 2),
        ("Обычная задача A", 3, 3),
        ("Обычная задача B", 3, 2),
        ("Фоновая задача", 4, 5)
    ]
    
    # Сортируем задачи по приоритету (чем меньше число — тем выше приоритет)
    sorted_tasks = sorted(tasks_with_priority, key=lambda x: x[1])
    
    # Ограничение: не более 2 задач одновременно
    semaphore = asyncio.Semaphore(2)
    
    # Создаём асинхронные задачи в порядке приоритета
    pending = [
        asyncio.create_task(scheduled_task(name, prio, dur, semaphore))
        for name, prio, dur in sorted_tasks
    ]
    
    results = []
    start_time = time.monotonic()
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Запуск планировщика...")
    
    while pending:
        done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
        for task in done:
            result = await task
            results.append(result)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Получен результат: {result}")

    total_time = time.monotonic() - start_time
    print(f"\nВсе задачи завершены! Общее время: {total_time:.2f} сек")
    print("Порядок завершения задач:")
    for i, res in enumerate(results, 1):
        print(f"  {i}. {res}")

asyncio.run(task6_async_scheduler())