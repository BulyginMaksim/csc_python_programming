import sqlite3


class DBHandler(object):

    def __init__(self, name):
        """Инициализация подключения к базы данных по названию файла."""
        self.db_name = name

    def request_lesson(self, request):
        """Этот метод отвечает за создание запроса и возвращение иероглифов по определенному названию урока."""
        cur = sqlite3.connect(self.db_name).cursor()
        cur = cur.execute("SELECT * FROM lessons WHERE lesson_name=? ORDER BY ID ASC", (request,)).fetchall()
        return {i: (v[2], v[3]) for i, v in enumerate(cur)}

    def request_name_lessons(self):
        """Этот этод отвечает за создание запроса и возвращение всех уникальных названий уроков."""
        cur = sqlite3.connect(self.db_name).cursor().execute("SELECT * FROM lessons").fetchall()
        return list(set(u[1] for u in cur))

