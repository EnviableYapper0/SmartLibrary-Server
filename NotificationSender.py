import abc
import requests
from email.message import EmailMessage
from smtplib import SMTP
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import atexit
import os

from model import *

LINE_NOTIFY_URL = 'https://notify-api.line.me/api/notify'


class NotificationSender(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def notify_successful_book_borrows(self, new_borrows):
        raise NotImplemented()

    @abc.abstractmethod
    def notify_book_in_circulation(self):
        raise NotImplemented()

    @staticmethod
    def compose_successful_book_borrow(new_borrows):
        user = new_borrows[0].user

        message_content = NotificationSender.get_header(user.name) + "You have the borrowed the following books: \n"
        for new_borrow in new_borrows:
            message_content += (new_borrow.book.title + ", due: " + str(new_borrow.due_time) + "\n")

        message_content = NotificationSender.write_end(message_content)
        return message_content

    @staticmethod
    def compose_book_in_circulation(query):
        to_compose = {}
        for book_circulation in query:
            if book_circulation.user not in to_compose.keys():
                to_compose[book_circulation.user] = []

            to_compose[book_circulation.user].append(book_circulation)

        messages_to_send = {}
        for user, book_circulation_list in to_compose.items():
            message_content = NotificationSender.get_header(user.name) + \
                              "You have yet to return the following book(s):\n"
            for book_circulation in book_circulation_list:
                due_time_str = str(book_circulation.due_time).split('.')[0]

                message_content += (book_circulation.book.title + ", due: " + due_time_str)

                if datetime.now() > book_circulation.due_time:
                    message_content += " (Overdue)"

                message_content += "\nYou can return the book by contacting the library's librarian.\n"

            message_content = NotificationSender.write_end(message_content)

            messages_to_send[user] = message_content

        return messages_to_send

    @staticmethod
    def get_header(name):
        return "Greetings, " + name + "\n\n"

    @staticmethod
    def write_end(content):
        return content + "\n\nSmartLibrary Staff"


class EmailSender(NotificationSender):

    def __init__(self):
        NotificationSender.__init__(self)

        host = os.environ["SMTP_HOST"]
        user = os.environ["SMTP_USER"]
        password = os.environ["SMTP_PASS"]

        self.smtp = SMTP(host=host)
        self.smtp.login(user=user, password=password)

    def notify_successful_book_borrows(self, new_borrows):
        user = new_borrows[0].user

        email_content = NotificationSender.compose_successful_book_borrow(new_borrows)

        msg = EmailMessage()
        msg.set_content(email_content)
        msg['Subject'] = "Notification of new borrows"
        msg['From'] = "noreply@smartlib.com"
        msg['To'] = user.email

        self.smtp.send_message(msg)

    def notify_book_in_circulation(self):
        users_with_email = User.select().where(User.email.is_null(False) & (User.is_active == True))

        query = BookCirculation.select().group_by(BookCirculation.user).\
            having((BookCirculation.user << users_with_email) & BookCirculation.return_time.is_null(True))

        emails_to_compose = NotificationSender.compose_book_in_circulation(query)

        for user, email_content in emails_to_compose.items():
            msg = EmailMessage()
            msg.set_content(email_content)
            msg['Subject'] = "Notification of books yet to be returned"
            msg['From'] = "noreply@smartlib.com"
            msg['To'] = user.email

            self.smtp.send_message(msg)

    def __del__(self):
        self.smtp.close()


class LineSender(NotificationSender):

    def notify_successful_book_borrows(self, new_borrows):
        user = new_borrows[0].user

        if user.line_token is None:
            return

        self.send_line_message(user.line_token, self.compose_successful_book_borrow(new_borrows))

    def notify_book_in_circulation(self):
        users_with_line = User.select().where(User.line_token.is_null(False) & (User.is_active == True))

        query = BookCirculation.select().group_by(BookCirculation.user). \
            having((BookCirculation.user << users_with_line) & BookCirculation.return_time.is_null(True))

        messages_to_send = NotificationSender.compose_book_in_circulation(query)

        for user, message in messages_to_send.items():
            self.send_line_message(user.line_token, message)

    @staticmethod
    def send_line_message(token, message):
        headers = {'content-type': 'application/x-www-form-urlencoded', 'Authorization': 'Bearer ' + token}
        requests.post(LINE_NOTIFY_URL, headers=headers, data={'message': message})


def send_not_returned_notification():
    EmailSender().notify_book_in_circulation()
    LineSender().notify_book_in_circulation()

    # avoid importing jsonify for just one return
    return "{ \"message\": \"Send completed\" }"


def register_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.start()
    scheduler.add_job(
        func=send_not_returned_notification,
        trigger=CronTrigger(hour=0, minute=0, second=0), # Run on midnight on every day.
        id='not_returned_notification',
        name='Send Notification for books that were being borrowed.',
        replace_existing=True)
    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    send_not_returned_notification()