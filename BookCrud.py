from flask_restful import Resource, fields, marshal_with
from flask import request

from BookManager import BookManager

book_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'isbn': fields.String,
    'added_on': fields.DateTime(dt_format='rfc822'),
    'is_available': fields.Boolean,
}


class AbstractBookCurd(Resource):
    def __init__(self):
        self.book_manager = BookManager()


class BookListCurd(AbstractBookCurd):
    @marshal_with(book_fields)
    def get(self):
        return self.book_manager.get_all_books()

    @marshal_with(book_fields)
    def post(self):
        args = request.get_json()
        return self.book_manager.add_book(args), 201


class BookCurd(AbstractBookCurd):
    @marshal_with(book_fields)
    def get(self, book_id):
        return self.book_manager.get_book(book_id)

    @marshal_with(book_fields)
    def put(self, book_id):
        args = request.get_json()
        return self.book_manager.update_book_data(book_id, args)