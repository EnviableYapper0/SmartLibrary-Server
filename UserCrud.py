from flask_restful import Resource, fields, marshal_with
from flask_restful.reqparse import request

from UserManager import UserManager

user_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'registered_on': fields.DateTime(dt_format='rfc822'),
    'is_active': fields.Boolean,
}


class AbstractUserCurd(Resource):
    def __init__(self):
        self.user_manager = UserManager()


class UserListCurd(AbstractUserCurd):
    @marshal_with(user_fields, envelope='resource')
    def get(self):
        return self.user_manager.get_all_user()

    @marshal_with(user_fields, envelope='resource')
    def post(self):
        args = request.get_json()
        return self.user_manager.register_new_user(args), 201


class UserCurd(AbstractUserCurd):
    @marshal_with(user_fields, envelope='resource')
    def get(self, user_id):
        return self.user_manager.get_specific_user(user_id)

    @marshal_with(user_fields, envelope='resource')
    def put(self, user_id):
        args = request.get_json()
        return self.user_manager.update_user_data(user_id, args)