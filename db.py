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
            curs.execute(statement, values or [])
            return curs

    def create_table(self, table_name:str, columns_dict:dict):
        '''Execute table creation with column type at columns_dict

        Arguments:
        table_name -- name of the table
        columns_dict -- dict with keys as columns names and values as data type, e.g. {'id': 'INTEGER PRIMARY KEY'}
        '''
        columns_str_list = [f'{k} {v}' for k, v in columns_dict.items()]
        values_str = ', '.join(columns_str_list)
        statement = f'CREATE TABLE IF NOT EXISTS {table_name} ({values_str});'
        self._execute(statement)

    def add(self, table_name:str, data:dict):
        '''Add data to table

        Arguments:
        table_name -- name of the table
        data -- dict with values to add, e.g. {'id': 2, 'name': 'Some title'}
        '''
        placeholder = ', '.join('?' * len(data))
        column_names = ', '.join(data.keys())
        column_values = tuple(data.values())

        self._execute(
            f'''
            INSERT INTO {table_name} 
            ({column_names})
            VALUES
            ({placeholder});
            ''',
            column_values,
        )

