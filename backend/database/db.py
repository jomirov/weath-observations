import sqlite3

class Sqlite3db:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)