from Database import database


class DatabaseManager(object):
    def __init__(self):
        self.db = database
        self.__opened_db_connection = not self.db.is_closed()
        if not self.__opened_db_connection:
            self.db.connect()

    @staticmethod
    def get_list(query):
        model_list = []

        for model in query:
            model_list.append(model)

        return model_list

    def __del__(self):
        if self.__opened_db_connection:
            self.db.close()