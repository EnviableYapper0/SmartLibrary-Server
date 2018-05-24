from Manager.DatabaseManager import DatabaseManager
from model import User
from Database import database


class UserManager(DatabaseManager):
    def __init__(self):
        DatabaseManager.__init__(self)
        User.create_table()

    def get_all_user(self):
        user_list = []

        for user in User.select():
            user_list.append(user)

        return user_list

    def register_new_user(self, json_data):
        return User.create(**json_data)

    def get_specific_user(self, user_id):
        return User.get((User.user_id == user_id) & (User.is_active == True))

    def get_user_by_rfid(self, rfid):
        return User.get((User.rfid == rfid) & (User.is_active == True))

    def update_user_data(self, user_id, json_data):
        if 'user_id' in json_data.keys() and json_data['user_id'] != user_id:
            raise IndexError("Id mismatched.")

        User.set_by_id(user_id, json_data)
        return self.get_specific_user(user_id)

    def mark_user_inactive(self, user_id):
        User.set_by_id(user_id, {"is_active": False})

    def update_user_line_token(self, user_id, line_token):
        User.set_by_id(user_id, {'line_token': line_token})