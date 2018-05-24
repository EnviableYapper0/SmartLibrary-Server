from flask import Flask
from flask_restful import Api
from peewee import IntegrityError

from Api.BookCirculationApi import BorrowApi, ReturnApi, BorrowHistoryApi
from Api.BookApi import BookListApi, BookApi, BookRfidApi
from Api.UserApi import UserListApi, UserApi, UserRfidApi, UserLineApi
import error_handler
from model import BaseModel
from RuleError import RuleError

app = Flask(__name__)
api = Api(app)


@app.route('/')
def hello_world():
    return 'Hello World!, this is a landing page for SmartLibrary.'


api.add_resource(BookListApi, '/book')
api.add_resource(BookApi, '/book/<int:book_id>')
api.add_resource(BookRfidApi, '/book/rfid/<rfid>')
api.add_resource(UserListApi, '/user')
api.add_resource(UserApi, '/user/<int:user_id>')
api.add_resource(UserLineApi, '/user/<int:user_id>/token')
api.add_resource(UserRfidApi, '/user/rfid/<rfid>')
api.add_resource(BorrowApi, '/borrow')
api.add_resource(ReturnApi, '/return/<int:borrow_id>')
api.add_resource(BorrowHistoryApi, '/history')

app.register_error_handler(IntegrityError, error_handler.bad_input_handler)
app.register_error_handler(IndexError, error_handler.index_error_handler)
app.register_error_handler(BaseModel.DoesNotExist, error_handler.does_not_exist)
app.register_error_handler(RuleError, error_handler.rule_error_handler)

if __name__ == '__main__':
    app.run()
