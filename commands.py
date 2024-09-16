from db import DatabaseManager
import sys
from datetime import datetime


db = DatabaseManager('bookmarks.db')


class CreateBookmarksTableCommand:
    def execute(self):
        db.create_table(
            'bookmarks',
            {
                'id': 'integer primary key autoincrement',
                'title': 'text not null',
                'url': 'text not null',
                'notes': 'text',
                'date_added': 'text not null',
            }
        )

class AddBookmarkCommand:
    def execute(self, data):
        '''
        Add bookmark to db

        Arguments:
        data -- (required) record data

        Returns
        success message
        '''
        data['date_added'] = datetime.utcnow().isoformat()
        db.add('bookmarks', data)
        return 'Bookmark added!'


class ListBookmarksCommand:
    def __init__(self, order_by: str = 'date_added'):
        self.order_by = order_by

    def execute(self) -> list:
        '''
        Execute `select` command from db manager

        Arguments:
        table_name -- name of the table
        order_by -- name of the column to sort by (default: 'date_added')

        Returns:
        list of rows of data
        '''
        return db.select('bookmarks', order_by=(self.order_by,)).fetchall()


class DeleteBookmarkCommand:
    def execute(self, data: str):
        '''
        Delete bookmark from db

        Arguments:
        data -- (required) record id

        Returns
        success message
        '''
        db.delete('bookmarks', {'id': data})
        return 'Bookmark deleted!'


class QuitCommand:
    def execute(self):
        sys.exit()
