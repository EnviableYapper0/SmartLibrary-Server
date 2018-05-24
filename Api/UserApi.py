from flask_restful import Resource, fields, marshal_with
from flask import request

from Manager.UserManager import UserManager

user_fields = {
    'user_id': fields.Integer,
    'name': fields.String,
    'registered_on': fields.DateTime(dt_format='rfc822'),
    'email': fields.String,
    'rfid': fields.String,
}


class AbstractUserApi(Resource):
    def __init__(self):
        self.user_manager = UserManager()


class UserListApi(AbstractUserApi):
    @marshal_with(user_fields)
    def get(self):
        return self.user_manager.get_all_user()

    @marshal_with(user_fields)
    def post(self):
        args = request.get_json()
        return self.user_manager.register_new_user(args), 201


class UserApi(AbstractUserApi):
    @marshal_with(user_fields)
    def get(self, user_id):
        return self.user_manager.get_specific_user(user_id)

    @marshal_with(user_fields)
    def put(self, user_id):
        args = request.get_json()
        return self.user_manager.update_user_data(user_id, args)

    def delete(self, user_id):
        self.user_manager.mark_user_inactive(user_id)


class UserRfidApi(AbstractUserApi):
    @marshal_with(user_fields)
    def get(self, rfid):
        return self.user_manager.get_user_by_rfid(rfid)


class UserLineApi(AbstractUserApi):
    def put(self, user_id):
        arg = request.get_json()
        self.user_manager.update_user_line_token(user_id, arg['line_token'])
