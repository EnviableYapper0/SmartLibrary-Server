from Database import database


class DatabaseManager(object):
    def __init__(self):
        self.db = database
        self.__opened_db_connection = not self.db.is_closed()
        if self.__opened_db_connection:
            self.db.connect()

    def __del__(self):
        if self.__opened_db_connection:
            self.db.close()