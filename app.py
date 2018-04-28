from flask import Flask
from flask_restful import Api
from peewee import IntegrityError

from BookCirculationApi import BorrowApi, ReturnApi
from BookApi import BookListApi, BookApi, BookRfidApi
from UserApi import UserListApi, UserApi, UserRfidApi
import error_handler

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!, this is a landing page for SmartLibrary.'


api.add_resource(BookListApi, '/book')
api.add_resource(BookApi, '/book/<book_id>')
api.add_resource(BookRfidApi, '/book/rfid/<rfid>')
api.add_resource(UserListApi, '/user')
api.add_resource(UserApi, '/user/<user_id>')
api.add_resource(UserRfidApi, '/user/rfid/<rfid>')
api.add_resource(BorrowApi, '/borrow')
api.add_resource(ReturnApi, '/return/<borrow_id>')

app.register_error_handler(IntegrityError, error_handler.bad_input_handler)
app.register_error_handler(IndexError, error_handler.index_error_handler)

if __name__ == '__main__':
    app.run()
