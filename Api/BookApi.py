from flask_restful import Resource, fields, marshal_with
from flask import request

from Manager.BookManager import BookManager

book_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'isbn': fields.String,
    'added_on': fields.DateTime(dt_format='rfc822'),
    'is_available': fields.Boolean,
}


class AbstractBookApi(Resource):
    def __init__(self):
        self.book_manager = BookManager()


class BookListApi(AbstractBookApi):
    @marshal_with(book_fields)
    def get(self):
        return self.book_manager.get_all_books()

    @marshal_with(book_fields)
    def post(self):
        args = request.get_json()
        return self.book_manager.add_book(args), 201


class BookApi(AbstractBookApi):
    @marshal_with(book_fields)
    def get(self, book_id):
        return self.book_manager.get_book(book_id)

    @marshal_with(book_fields)
    def put(self, book_id):
        args = request.get_json()
        return self.book_manager.update_book_data(book_id, args)


class BookRfidApi(AbstractBookApi):
    @marshal_with(book_fields)
    def get(self, rfid):
        return self.book_manager.get_book_by_rfid(rfid)