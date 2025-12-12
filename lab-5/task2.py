import threading
import time
import random

def download_file(filename, size):
    """
    Имитирует загрузку файла
    
    Параметры:
    filename (str): имя файла
    size (int): размер файла в МБ
    """
    download_time = size * 0.1  # 0.1 сек на МБ
    print(f"Начало загрузки {filename} ({size} МБ)")
    
    # Имитация прогресса загрузки
    for i in range(5):
        time.sleep(download_time / 5)
        progress = (i + 1) * 20
        print(f"{filename}: {progress}% загружено")
    
    print(f"Завершена загрузка {filename}")

def task2_threaded_downloader():
    """
    Задача: Реализуйте многопоточную загрузку файлов.
    Файлы для загрузки:
    1. "document.pdf" - 10 МБ
    2. "image.jpg" - 5 МБ  
    3. "video.mp4" - 20 МБ
    4. "archive.zip" - 15 МБ
    
    Требуется:
    - Загрузить все файлы параллельно в разных потоках
    - Измерить общее время выполнения
    - Убедиться, что все потоки завершились
    """
    files = [
        ("document.pdf", 10),
        ("image.jpg", 5),
        ("video.mp4", 20),
        ("archive.zip", 15)
    ]
    
    start_time = time.time()
    threads = []
    
    for filename, size in files:
        thread = threading.Thread(target=download_file, args=(filename, size))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()
    
    end_time = time.time()
    print(f"Общее время загрузки: {end_time - start_time:.2f} секунд")

task2_threaded_downloader()