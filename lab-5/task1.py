import time

def sync_calculate(operation, a, b, delay):
    """
    Выполняет математическую операцию с задержкой
    
    Параметры:
    operation (str): тип операции ('+', '-', '*', '/')
    a, b (float): числа для операции
    delay (float): время имитации вычислений
    
    Возвращает:
    float: результат операции
    """
    print(f"Начало операции {a} {operation} {b}")
    time.sleep(delay)  # Имитация долгого вычисления
    
    if operation == '+':
        result = a + b
    elif operation == '-':
        result = a - b
    elif operation == '*':
        result = a * b
    elif operation == '/':
        result = a / b if b != 0 else 'Ошибка: деление на ноль'
    else:
        result = 'Неизвестная операция'
    
    print(f"Конец операции {a} {operation} {b} = {result}")
    return result

def task1_sync_calculations():
    """
    Задача: Выполните последовательно 4 операции и измерьте общее время выполнения.
    Операции:
    1. 15 + 25 с задержкой 2 секунды
    2. 40 - 18 с задержкой 1 секунда  
    3. 12 * 8 с задержкой 3 секунды
    4. 100 / 5 с задержкой 1 секунда
    
    Требуется:
    - Вывести общее время выполнения
    - Вывести результаты всех операций
    """
    start_time = time.time()
    
    results = []
    results.append(sync_calculate('+', 15, 25, 2))
    results.append(sync_calculate('-', 40, 18, 1))
    results.append(sync_calculate('*', 12, 8, 3))
    results.append(sync_calculate('/', 100, 5, 1))
    
    end_time = time.time()
    print(f"Общее время выполнения: {end_time - start_time:.2f} секунд")
    print(f"Результаты: {results}")

task1_sync_calculations()