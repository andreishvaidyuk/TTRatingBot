# -*- coding: utf-8 -*-

class SQLighter:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def select_all(self):
        """Получаем все строки"""
        with self.connection:
            return self.cursor.execute('SELECT * from RatingDB').fetchall()

    def select_single(self, rownum):
        """Получаем одну строку с номером rownum"""
        with self.connection:
            return self.cursor.execute('SELECT * from RatingDB where file_id=?', (rownum, )).fetchall()[0]

    def count_rows(self):
        """Считаем количество строк"""
        with self.connection:
            result = self.cursor.execute('SELECT * from RatingDB').fetchall()
            return len(result)

    def close(self):
        """Закрываем текущее соединение с БД"""
        self.connection.close()