import sqlite3


class DatabaseManager:
    def __init__(self, db_filename:str):
        self.connection = sqlite3.connect(db_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement:str, values:list|tuple=None):
        '''Execute statement on connection

        Arguments:
        statement -- contains string, may content placeholders, e.g. "(?, ?)"
        values -- data to replace placeholders in statement (default: None)
        '''
        with self.connection:
            curs = self.connection.cursor()
            curs.execute(statement)
            return curs

