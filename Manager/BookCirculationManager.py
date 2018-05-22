from threading import Thread

from NotificationSender import EmailSender, LineSender
from model import BookCirculation, Book, User
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

    def borrows(self, dataList):
        successful_borrows = []

        with database.atomic():
            for data in dataList:
                book = Book.get_by_id(data["book"]["book_id"])
                user = User.get_by_id(data["user"]["user_id"])
                data['book'] = book
                data['user'] = user

                successful_borrows.append(BookCirculation.create(**data))

        SendBorrowNotification(successful_borrows).start()

        return successful_borrows

    def return_book(self, borrow_id, return_time=datetime.now()):
        BookCirculation.update(return_time=return_time).where(BookCirculation.borrow_id == borrow_id).execute()
        return self.get_specific_record(borrow_id)

    def __del__(self):
        database.close()


class SendBorrowNotification(Thread):
    def __init__(self, new_borrows):
        Thread.__init__(self)
        self.new_borrows = new_borrows

    def run(self):
        notification_senders = [EmailSender(), LineSender()]

        for notification_sender in notification_senders:
            notification_sender.notify_successful_book_borrows(self.new_borrows)