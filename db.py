import sqlite3


class DatabaseManager:
    def __init__(self, db_filename):
        self.connection = sqlite3.connect(db_filename)

    def __del__(self):
        self.connection.close()

