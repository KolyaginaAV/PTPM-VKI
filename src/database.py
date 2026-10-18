import sqlite3


class TriangleDatabase:
    def __init__(self, db_path=":memory:"): #:memory: - cпециальный «путь», который говорит SQLite: «храни базу в
                                            #оперативной памяти»; база исчезает при завершении программы,
                                            #каждый тест получает чистую базу
        self.conn = sqlite3.connect(db_path) #соединение с БД
        self.cursor = self.conn.cursor()   #cursor - объект, через который отправляются SQL-команды в бд
        self._create_table()  #вызывает метод создания таблицы (если её нет)

    def _create_table(self): #подчёркивание в начале - «внутренний метод, не для вызова снаружи». Он нужен только классу
        #execute - выполни
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS triangles (
                a REAL, b REAL, c REAL, 
                type TEXT, error TEXT,
                PRIMARY KEY (a, b, c)
            )
        """)
        #IF NOT EXISTS - создай таблицу, только если её ещё нет
        #REAL - вещественное число
        self.conn.commit() #фиксирует изменения

    def add_record(self, a, b, c, triangle_type, error_msg):
        self.cursor.execute(
            "INSERT OR REPLACE INTO triangles (a, b, c, type, error) VALUES (?, ?, ?, ?, ?)",
            (a, b, c, triangle_type, error_msg)
        )
        #INSERT — вставить новую запись
        #EPLACE — если запись с таким PRIMARY KEY (комбинацией a, b, c) уже есть, заменить её новой
        #VALUES (?, ?, ?, ?, ?) — параметры запроса. Знаки ? — это «заполнители». Значения передаются вторым
        #аргументом (a, b, c, triangle_type, error_msg)
        self.conn.commit()

    def get_record(self, a, b, c):
        self.cursor.execute("SELECT type, error FROM triangles WHERE a=? AND b=? AND c=?", (a, b, c))
        return self.cursor.fetchone() #берёт одну (первую) строку из результата
        #SELECT type, error — выбери колонки type и error
        #Возвращает кортеж: ("разносторонний", ""), eсли запись не найдена — возвращает None

    def delete_record(self, a, b, c):
        self.cursor.execute("DELETE FROM triangles WHERE a=? AND b=? AND c=?", (a, b, c))
        self.conn.commit()
