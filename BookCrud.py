from BookManager import BookManager
from flask_restful import reqparse, Resource
from flask import jsonify


class BookCurd(Resource):
    def __init__(self):
        self.book_manager = BookManager()
        self.parser = reqparse.RequestParser()

    def get(self):
        return jsonify(self.book_manager.get_all_books())

    def post(self):
        self.parser.add_argument('name', type=str, help="Name of the book.")
        self.parser.add_argument('isbn', type=str, help="The book's ISBN.")
        arg = self.parser.parse_args()
        return jsonify(self.book_manager.add_book(arg))
