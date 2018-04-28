from model import BookCirculation
from Manager.BookManager import BookManager
from Manager.UserManager import UserManager
from Database import database
from datetime import datetime


class BookCirculationManager:
    def __init__(self):
        database.connect()
        BookCirculation.create_table()

    def get_complete_history(self):
        complete_history = []

        for book_circulation in BookCirculation.select():
            complete_history.append(book_circulation)

        return complete_history

    def get_all_being_borrowed(self):
        being_borrowed = []

        for book_circulation in BookCirculation.select().where(BookCirculation.return_time == None):
            being_borrowed.append(book_circulation)

        return being_borrowed

    def get_specific_record(self, borrow_id):
        return BookCirculation.get_by_id(borrow_id)

    def borrow(self, json_data):
        book = BookManager().get_book(json_data['book']['id'])
        user = UserManager().get_specific_user(json_data['user']['id'])
        del json_data['book']
        del json_data['user']

        return BookCirculation.create(book=book, user=user, **json_data)

    def return_book(self, borrow_id, return_time=datetime.now()):
        BookCirculation.update(return_time=return_time).where(BookCirculation.id==borrow_id).execute()
        return self.get_specific_record(borrow_id)

    def __del__(self):
        database.close()