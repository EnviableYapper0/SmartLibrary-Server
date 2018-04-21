from flask import Flask
from flask_restful import Api
from peewee import IntegrityError

from BookCirculationCrud import BorrowApi, ReturnApi
from BookCrud import BookListCurd, BookCurd, BookRfidCurd
from UserCrud import UserListCurd, UserCurd, UserRfidCurd
import error_handler

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

app.register_error_handler(IntegrityError, error_handler.bad_input_handler)
app.register_error_handler(IndexError, error_handler.index_error_handler)

if __name__ == '__main__':
    app.run()
