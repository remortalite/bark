import sqlite3
from typing import Union


class DatabaseManager:
    def __init__(self, db_filename: str):
        self.connection = sqlite3.connect(db_filename)

    def __del__(self):
        self.connection.close()

    def _execute(self, statement: str, values: (list | tuple) = None):
        '''Execute statement on connection

        Arguments:
        statement -- contains string, may content placeholders, e.g. "(?, ?)"
        values -- data to replace placeholders in statement (default: None)
        '''
        with self.connection:
            curs = self.connection.cursor()
            curs.execute(statement, values or [])
            return curs

    def create_table(self, table_name: str, columns_dict: dict):
        '''Execute table creation with column type at columns_dict

        Arguments:
        table_name -- name of the table
        columns_dict -- dict with keys as columns names and values as
                        data type, e.g. {'id': 'INTEGER PRIMARY KEY'}
        '''
        columns_str_list = [f'{k} {v}' for k, v in columns_dict.items()]
        values_str = ', '.join(columns_str_list)
        statement = f'CREATE TABLE IF NOT EXISTS {table_name} ({values_str});'
        self._execute(statement)

    def add(self, table_name: str, data: dict):
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

    def delete(self, table_name: str, criteria: dict):
        '''Delete data from table with specified criteria

        Arguments:
        table_name -- name of the table
        criteria -- a dict with parameters of the record to
                    delete, i.e. WHERE clause of SQL (e.g. {'id': 1}).
        '''
        placeholder = [f'{column} = ?' for column in criteria.keys()]
        delete_criteria = ' AND '.join(placeholder)
        statement = f'DELETE FROM {table_name} WHERE {delete_criteria}'
        self._execute(statement, tuple(criteria.values()))

    def select(self, table_name: str,
               criteria: Union[dict, None] = None,
               order_by: Union[list, None] = None) -> sqlite3.Cursor:
        '''Select data from table with optional criteria and ordering

        Arguments:
        table_name -- name of the table
        criteria -- (optional) a dict with parameters of the record to
                    fetch, i.e. WHERE clause of SQL (e.g. {'id': 1})
        order_by -- (optional) a list with column names for ordering
                    to use, i.e. ORDER BY clause (e.g. ['id'])
        '''
        criteria = criteria or {}
        query = f"SELECT * FROM {table_name}"
        if criteria:
            placeholder_criteria = [f"{column} = ?" for column in criteria.keys()]
            select_criteria = ' AND '.join(placeholder_criteria)
            query += f' WHERE {select_criteria}'
        if order_by:
            ordering = ', '.join(order_by or [])
            query += f' ORDER BY {ordering}'
        return self._execute(query, tuple(criteria.values()))