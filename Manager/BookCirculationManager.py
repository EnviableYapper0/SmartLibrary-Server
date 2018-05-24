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
        return DatabaseManager.get_list(BookCirculation.select())

    def get_all_being_borrowed(self):
        return DatabaseManager.get_list(
            BookCirculation.select().where(BookCirculation.return_time.is_null(True))
        )

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

    def __search_user(self, keyword: str):
        return User.select().where((User.name.contains(keyword)) & (User.is_active == True))

    def __search_book(self, keyword: str):
        return Book.select().where((Book.title.contains(keyword)) & (Book.is_available == True))

    def search_borrowing(self, keyword: str):
        user_query = self.__search_user(keyword)
        book_query = self.__search_book(keyword)

        return DatabaseManager.get_list(
            BookCirculation.select().where(((BookCirculation.user << user_query) |
                                            (BookCirculation.book << book_query)) &
                                           BookCirculation.return_time.is_null(True))
        )

    def search_history(self, keyword: str):
        user_query = self.__search_user(keyword)
        book_query = self.__search_book(keyword)

        return DatabaseManager.get_list(
            BookCirculation.select().where((BookCirculation.user << user_query) | (BookCirculation.book << book_query))
        )

    def return_book(self, borrow_id: int):
        BookCirculation.set_by_id(borrow_id, {"return_time": datetime.now()})


class SendBorrowNotification(Thread):
    def __init__(self, new_borrows):
        Thread.__init__(self)
        self.new_borrows = new_borrows

    def run(self):
        notification_senders = [EmailSender(), LineSender()]

        for notification_sender in notification_senders:
            notification_sender.notify_successful_book_borrows(self.new_borrows)
