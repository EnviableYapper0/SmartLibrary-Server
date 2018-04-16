from flask import Flask
from flask_restful import Api
from BookCrud import BookListCurd, BookCurd
from model import Book

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!, this is a landing page for SmartLibrary.'


api.add_resource(BookListCurd, '/book')
api.add_resource(BookCurd, '/book/<book_id>')

if __name__ == '__main__':
    Book.create_table()
    app.run()
