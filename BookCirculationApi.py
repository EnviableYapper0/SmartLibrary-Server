from BookCirculationManager import BookCirculationManager
from flask_restful import Resource, fields, marshal_with
from flask import request
from BookApi import book_fields
from UserApi import user_fields

book_circulation_fields = {
    'id': fields.Integer,
    'book': fields.Nested(book_fields),
    'user': fields.Nested(user_fields),
    'borrow_time': fields.DateTime(dt_format='rfc822'),
    'due_time': fields.DateTime(dt_format='rfc822'),
    'return_time': fields.DateTime(dt_format='rfc822'),
}


class AbstractCirculationApi(Resource):
    def __init__(self):
        self.book_circulation_manager = BookCirculationManager()


class BorrowApi(AbstractCirculationApi):
    @marshal_with(book_circulation_fields)
    def post(self):
        args = request.get_json()
        return self.book_circulation_manager.borrow(args)


class ReturnApi(AbstractCirculationApi):
    @marshal_with(book_circulation_fields)
    def put(self, borrow_id):
        args = request.get_json()
        return self.book_circulation_manager.return_book(borrow_id, args['return_time'])