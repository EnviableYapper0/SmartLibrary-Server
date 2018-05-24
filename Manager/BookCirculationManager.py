from threading import Thread

from Manager.DatabaseManager import DatabaseManager
from NotificationSender import EmailSender, LineSender
from RuleError import RuleError
from model import BookCirculation, Book, User
from Database import database
from datetime import datetime


class BookCirculationManager(DatabaseManager):

    def __init__(self):
        DatabaseManager.__init__(self)
        BookCirculation.create_table()

    def get_complete_history(self):
        complete_history = []

        for book_circulation in BookCirculation.select():
            complete_history.append(book_circulation)

        return complete_history

    def get_all_being_borrowed(self):
        being_borrowed = []

        for book_circulation in BookCirculation.select().where(BookCirculation.return_time.is_null(True)):
            being_borrowed.append(book_circulation)

        return being_borrowed

    def get_specific_record(self, borrow_id):
        return BookCirculation.get_by_id(borrow_id)

    def borrows(self, data_list):
        successful_borrows = []
        user = User.get_by_id(data_list[0]["user"]["user_id"])

        with database.atomic():
            num_book_borrowing = BookCirculation.select().where((BookCirculation.user == user) &
                                                                (BookCirculation.return_time.is_null(True))).count()

            if num_book_borrowing + len(data_list) > 5:
                raise RuleError("Number is borrowing books exceeded.")

            for data in data_list:
                book = Book.get_by_id(data["book"]["book_id"])
                data['book'] = book
                data['user'] = user

                if BookCirculation.select().where((BookCirculation.book == book) &
                                                  (BookCirculation.return_time.is_null(True))).count() != 0:
                    raise RuleError("The book has already been borrowed.")

                successful_borrows.append(BookCirculation.create(**data))

        SendBorrowNotification(successful_borrows).start()

        return successful_borrows

    def return_book(self, borrow_id:int):
        BookCirculation.set_by_id(borrow_id, {"return_time": datetime.now()})


class SendBorrowNotification(Thread):
    def __init__(self, new_borrows):
        Thread.__init__(self)
        self.new_borrows = new_borrows

    def run(self):
        notification_senders = [EmailSender(), LineSender()]

        for notification_sender in notification_senders:
            notification_sender.notify_successful_book_borrows(self.new_borrows)