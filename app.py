from flask import Flask
from flask_restful import Api
from BookCrud import BookListCurd, BookCurd, BookRfidCurd
from UserCrud import UserListCurd, UserCurd, UserRfidCurd
from BookCirculationCrud import BorrowApi, ReturnApi
from model import Book, User, BookCirculation

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!, this is a landing page for SmartLibrary.'


api.add_resource(BookListCurd, '/book')
api.add_resource(BookCurd, '/book/<book_id>')
api.add_resource(BookRfidCurd, '/book/rfid/<rfid>')
api.add_resource(UserListCurd, '/user')
api.add_resource(UserCurd, '/user/<user_id>')
api.add_resource(UserRfidCurd, '/user/rfid/<rfid>')
api.add_resource(BorrowApi, '/borrow')
api.add_resource(ReturnApi, '/return/<borrow_id>')

if __name__ == '__main__':
    app.run()
