from model import User
from Database import database


class UserManager(object):
    def __init__(self):
        database.connect()
        User.create_table()

    def get_all_user(self):
        user_list = []

        for user in User.select():
            user_list.append(user)

        return user_list

    def register_new_user(self, json_data):
        return User.create(**json_data)

    def get_specific_user(self, user_id):
        return User.get_by_id(user_id)

    def get_user_by_rfid(self, rfid):
        return User.get(User.rfid == rfid)

    def update_user_data(self, user_id, json_data):
        if 'id' in json_data and json_data['id'] != user_id:
            raise IndexError("Id mismatched.")

        User.update(**json_data).where(User.id == user_id).execute()
        return self.get_specific_user(user_id)

    def __del__(self):
        database.close()