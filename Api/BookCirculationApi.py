from Manager.BookCirculationManager import BookCirculationManager
from flask_restful import Resource, fields, marshal_with
from flask import request
from Api.BookApi import book_fields
from Api.UserApi import user_fields

book_circulation_fields = {
    'borrow_id': fields.Integer,
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
    def get(self):
        return self.book_circulation_manager.get_all_being_borrowed()

    @marshal_with(book_circulation_fields)
    def post(self):
        args = request.get_json()
        return self.book_circulation_manager.borrows(args)


class ReturnApi(AbstractCirculationApi):
    def delete(self, borrow_id):
        self.book_circulation_manager.return_book(borrow_id)


class BorrowHistoryApi(AbstractCirculationApi):
    @marshal_with(book_circulation_fields)
    def get(self):
        return self.book_circulation_manager.get_complete_history()


class BorrowSearchApi(AbstractCirculationApi):
    @marshal_with(book_circulation_fields)
    def get(self, keyword):
        return self.book_circulation_manager.search_borrowing(keyword)


class HistorySearchApi(AbstractCirculationApi):
    @marshal_with(book_circulation_fields)
    def get(self, keyword):
        return self.book_circulation_manager.search_history(keyword)