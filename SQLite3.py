import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """ Получаем все строки """
        with self.connection:
            return self.cursor.execute('SELECT * FROM Schedule').fetchall()

    def write_to(self, chat_id, user_id, username, dayofweek):
        sqlite_insert_with_param = """INSERT INTO Schedule
                                 (ChatID, UserID, User, DayOfWeek) 
                                 VALUES (?, ?, ?, ?);"""

        data_tuple = (chat_id, user_id, username, dayofweek)
        self.cursor.execute(sqlite_insert_with_param, data_tuple)
        self.connection.commit()
        print("Python Variables inserted successfully into SqliteDb_developers table")


    def read_my_data(self, username):
        with self.connection:
            return self.cursor.execute('''SELECT s.DayOfWeek FROM Schedule s
                                        WHERE s.User = ?''', [username]).fetchall()


    def getID(self, user_id):
        with self.connection:
            return self.cursor.execute('''SELECT  ChatID FROM Schedule WHERE UserID=? LIMIT 1''', [user_id]).fetchall()

    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()