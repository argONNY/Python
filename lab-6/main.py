import sqlite3
from datetime import datetime, date
from contextlib import contextmanager


class LibraryManager:
    def __init__(self, db_path='library.db'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Инициализация базы данных и таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица книг
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    author TEXT NOT NULL,
                    year INTEGER,
                    genre TEXT,
                    is_available BOOLEAN DEFAULT 1
                )
            ''')
            
            # Таблица читателей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS readers (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE,
                    phone TEXT,
                    registration_date DATE DEFAULT CURRENT_DATE
                )
            ''')
            
            # Таблица выдач
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS borrowings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    reader_id INTEGER NOT NULL,
                    borrow_date DATE DEFAULT CURRENT_DATE,
                    return_date DATE,
                    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
                    FOREIGN KEY (reader_id) REFERENCES readers(id) ON DELETE CASCADE
                )
            ''')
            
            conn.commit()
    
    @contextmanager
    def _get_connection(self):
        """Контекстный менеджер для подключения к БД с настройкой row_factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        except Exception:
            conn.rollback()
            raise
        else:
            conn.commit()
        finally:
            conn.close()
    
    def add_book(self, title, author, year=None, genre=None):
        """Добавить новую книгу в библиотеку"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO books (title, author, year, genre) 
                    VALUES (?, ?, ?, ?)
                ''', (title, author, year, genre))
                book_id = cursor.lastrowid
                print(f"Книга '{title}' добавлена с ID {book_id}")
                return book_id
        except sqlite3.IntegrityError as e:
            print(f"Ошибка при добавлении книги: {e}")
            return None
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            return None
    
    def add_reader(self, name, email=None, phone=None):
        """Зарегистрировать нового читателя"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO readers (name, email, phone) 
                    VALUES (?, ?, ?)
                ''', (name, email, phone))
                reader_id = cursor.lastrowid
                print(f"Читатель '{name}' зарегистрирован с ID {reader_id}")
                return reader_id
        except sqlite3.IntegrityError as e:
            print(f"Ошибка: Email '{email}' уже зарегистрирован")
            return None
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            return None
    
    def borrow_book(self, book_id, reader_id):
        """
        Выдать книгу читателю
        - Проверить, что книга доступна
        - Обновить статус книги
        - Создать запись о выдаче
        - Использовать транзакцию
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Получаем информацию о книге и читателе
                cursor.execute("SELECT title, is_available FROM books WHERE id = ?", (book_id,))
                book = cursor.fetchone()
                cursor.execute("SELECT name FROM readers WHERE id = ?", (reader_id,))
                reader = cursor.fetchone()
                
                if not book:
                    raise ValueError(f"Книга с ID {book_id} не найдена")
                if not reader:
                    raise ValueError(f"Читатель с ID {reader_id} не найден")
                
                if not book['is_available']:
                    raise ValueError("Книга уже выдана другому читателю")
                
                # Выдаем книгу
                cursor.execute("UPDATE books SET is_available = 0 WHERE id = ?", (book_id,))
                cursor.execute(
                    "INSERT INTO borrowings (book_id, reader_id) VALUES (?, ?)",
                    (book_id, reader_id)
                )
                
                borrowing_id = cursor.lastrowid
                print(f"Книга '{book['title']}' успешно выдана читателю {reader['name']}")
                return borrowing_id
                
        except ValueError as e:
            print(f"Ошибка: {e}")
            return None
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            return None
    
    def return_book(self, borrowing_id):
        """
        Вернуть книгу в библиотеку
        - Обновить статус книги
        - Установить дату возврата
        - Использовать транзакцию
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                # Получаем информацию о выдаче
                cursor.execute('''
                    SELECT b.id as book_id, b.title, r.name as reader_name
                    FROM borrowings br
                    JOIN books b ON br.book_id = b.id
                    JOIN readers r ON br.reader_id = r.id
                    WHERE br.id = ? AND br.return_date IS NULL
                ''', (borrowing_id,))
                borrowing = cursor.fetchone()
                
                if not borrowing:
                    raise ValueError("Выдача не найдена или книга уже возвращена")
                
                # Возвращаем книгу
                cursor.execute("UPDATE books SET is_available = 1 WHERE id = ?", (borrowing['book_id'],))
                cursor.execute(
                    "UPDATE borrowings SET return_date = CURRENT_DATE WHERE id = ?",
                    (borrowing_id,)
                )
                
                print(f"Книга '{borrowing['title']}' возвращена в библиотеку")
                return True
                
        except ValueError as e:
            print(f"Ошибка: {e}")
            return False
        except sqlite3.Error as e:
            print(f"Ошибка базы данных: {e}")
            return False
    
    def find_available_books(self, author=None, genre=None):
        """Найти доступные книги (с фильтрацией по автору/жанру)"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                query = "SELECT * FROM books WHERE is_available = 1"
                params = []
                
                if author:
                    query += " AND author LIKE ?"
                    params.append(f"%{author}%")
                if genre:
                    query += " AND genre LIKE ?"
                    params.append(f"%{genre}%")
                
                cursor.execute(query, params)
                books = [dict(row) for row in cursor.fetchall()]
                return books
                
        except sqlite3.Error as e:
            print(f"Ошибка при поиске книг: {e}")
            return []
    
    def get_reader_borrowings(self, reader_id):
        """Получить список текущих выдач читателя"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT br.id, b.title, b.author, br.borrow_date
                    FROM borrowings br
                    JOIN books b ON br.book_id = b.id
                    WHERE br.reader_id = ? AND br.return_date IS NULL
                ''', (reader_id,))
                
                borrowings = [dict(row) for row in cursor.fetchall()]
                return borrowings
                
        except sqlite3.Error as e:
            print(f"Ошибка при получении выдач читателя: {e}")
            return []
    
    def get_overdue_borrowings(self, days=30):
        """Найти просроченные выдачи (больше N дней)"""
        try:
            with self._get_connection() as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT br.id, b.title, r.name as reader_name, br.borrow_date
                    FROM borrowings br
                    JOIN books b ON br.book_id = b.id
                    JOIN readers r ON br.reader_id = r.id
                    WHERE br.return_date IS NULL 
                    AND date(br.borrow_date) < date('now', '-' || ? || ' days')
                ''', (days,))
                
                overdue = [dict(row) for row in cursor.fetchall()]
                return overdue
                
        except sqlite3.Error as e:
            print(f"Ошибка при поиске просроченных выдач: {e}")
            return []


def main():
    library = LibraryManager()
    
    # Добавляем книги
    library.add_book("Преступление и наказание", "Федор Достоевский", 1866, "Роман")
    library.add_book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман")
    library.add_book("1984", "Джордж Оруэлл", 1949, "Антиутопия")
    
    # Регистрируем читателей
    library.add_reader("Иван Иванов", "ivan@mail.com", "+79161234567")
    library.add_reader("Петр Петров", "petr@mail.com", "+79167654321")
    
    # Выдаем книги
    library.borrow_book(1, 1)  # Иван берет "Преступление и наказание"
    library.borrow_book(2, 2)  # Петр берет "Мастер и Маргарита"
    
    # Пытаемся выдать уже занятую книгу
    try:
        library.borrow_book(1, 2)  # Должна быть ошибка
    except Exception as e:
        print(f"Ошибка: {e}")
    
    # Ищем доступные книги
    available = library.find_available_books(author="Джордж Оруэлл")
    print("Доступные книги Оруэлла:", available)
    
    # Возвращаем книгу
    library.return_book(1)
    
    # Проверяем, что книга снова доступна
    available = library.find_available_books()
    print("Все доступные книги:")
    for book in available:
        print(f"  - {book['title']} ({book['author']})")


if __name__ == "__main__":
    main()