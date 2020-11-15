import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM Schedule').fetchall()

    def write_to(self, username, name, dayofweek):
        sqlite_insert_with_param = """INSERT INTO Schedule
                                 (User, Name, DayOfWeek) 
                                 VALUES (?, ?, ?);"""

        data_tuple = (username, name, dayofweek)
        self.cursor.execute(sqlite_insert_with_param, data_tuple)
        self.connection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()