from flask import Flask
from flask_restful import Api
from BookCrud import BookListCurd, BookCurd
from UserCrud import UserListCurd, UserCurd
from BookCirculationCrud import BorrowApi, ReturnApi
from model import Book, User, BookCirculation

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!, this is a landing page for SmartLibrary.'


api.add_resource(BookListCurd, '/book')
api.add_resource(BookCurd, '/book/<book_id>')
api.add_resource(UserListCurd, '/user')
api.add_resource(UserCurd, '/user/<user_id>')
api.add_resource(BorrowApi, '/borrow')
api.add_resource(ReturnApi, '/return/<borrow_id>')

if __name__ == '__main__':
    Book.create_table()
    User.create_table()
    BookCirculation.create_table()
    app.run()
