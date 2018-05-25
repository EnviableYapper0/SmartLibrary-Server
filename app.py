from flask import Flask
from flask_restful import Api
from peewee import IntegrityError

from Api.BookCirculationApi import *
from Api.BookApi import *
from Api.UserApi import *
from ErrorHandling import error_handler
from peewee import DoesNotExist
from ErrorHandling.RuleError import RuleError
from NotificationSender import send_not_returned_notification

app = Flask(__name__)
api = Api(app, catch_all_404s=True)


@app.route('/')
def hello_world():
    return 'Hello World!, this is a landing page for SmartLibrary.'


api.add_resource(BookListApi, '/book')
api.add_resource(BookApi, '/book/<int:book_id>')
api.add_resource(BookRfidApi, '/book/rfid/<rfid>')
api.add_resource(BookSearchApi, '/book/search/<keyword>')

api.add_resource(UserListApi, '/user')
api.add_resource(UserApi, '/user/<int:user_id>')
api.add_resource(UserLineApi, '/user/<int:user_id>/token')
api.add_resource(UserRfidApi, '/user/rfid/<rfid>')
api.add_resource(UserSearchApi, '/user/search/<keyword>')

api.add_resource(BorrowApi, '/borrow')
api.add_resource(ReturnApi, '/return/<int:borrow_id>')
api.add_resource(BorrowHistoryApi, '/history')
api.add_resource(BorrowSearchApi, '/borrow/search/<keyword>')
api.add_resource(HistorySearchApi, '/history/search/<keyword>')

# Workaround to prevent flask-restful from taking over
app.config['PROPAGATE_EXCEPTIONS'] = True

app.register_error_handler(IntegrityError, error_handler.error_handler)
app.register_error_handler(IndexError, error_handler.index_error_handler)
app.register_error_handler(DoesNotExist, error_handler.does_not_exist)
app.register_error_handler(RuleError, error_handler.rule_error_handler)
app.register_error_handler(Exception, error_handler.custom_message_error_handler)


app.add_url_rule('/manual_notification', 'send_not_returned_notification', send_not_returned_notification)


if __name__ == '__main__':
    app.run()
