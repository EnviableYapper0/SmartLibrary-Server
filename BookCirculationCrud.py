from BookCirculationManager import BookCirculationManager
from flask_restful import Resource, fields, marshal_with
from flask import request
from BookCrud import book_fields
from UserCrud import user_fields

book_circulation_fields = {
    'id': fields.Integer,
    'book': fields.Nested(book_fields),
    'user': fields.Nested(user_fields),
    'borrow_time': fields.DateTime(dt_format='rfc822'),
    'return_time': fields.DateTime(dt_format='rfc822'),
}


class AbstractCirculationCurd(Resource):
    def __init__(self):
        self.book_circulation_manager = BookCirculationManager()


class BorrowApi(AbstractCirculationCurd):
    @marshal_with(book_circulation_fields)
    def post(self):
        args = request.get_json()
        return self.book_circulation_manager.borrow(args)


class ReturnApi(AbstractCirculationCurd):
    @marshal_with(book_circulation_fields)
    def put(self, borrow_id):
        args = request.get_json()
        return self.book_circulation_manager.return_book(borrow_id, args['return_time'])