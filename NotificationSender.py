import abc
from email.message import EmailMessage
from smtplib import SMTP


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
        for user, book_circulation_list in to_compose:
            message_content = NotificationSender.get_header(user.name) + "You have yet to return the following book(s):"
            for book_circulation in book_circulation_list:
                message_content += (book_circulation.book.title + ", due: " + str(book_circulation.due_time))

                if datetime.now() > book_circulation.due_time:
                    message_content += " (Overdue)"

                message_content += "\n"

            message_content = "You may extend the borrowing period at the kiosk."
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
        self.smtp = SMTP(host='smtp.mailtrap.io', port=2525)
        self.smtp.login('3f534eda171e91', '3ab5f8fea23d28')

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
        query = BookCirculation.select().group_by(BookCirculation.user).\
            having((BookCirculation.user.email is not None) | (BookCirculation.return_time is None))

        emails_to_compose = NotificationSender.compose_book_in_circulation(query)

        for user, email_content in emails_to_compose:
            msg = EmailMessage()
            msg.set_content(email_content)
            msg['Subject'] = "Notification of books yet to be returned"
            msg['From'] = "noreply@smartlib.com"
            msg['To'] = user.email

            self.smtp.send_message(msg)

    def __del__(self):
        self.smtp.close()


if __name__ == '__main__':
    from model import *
    book1 = Book(id=1, title="Windows 10 Plain & Simple, 2nd Edition", isbn="978-1-5093-0673-2")
    book2 = Book(id=2, title="Beyond Bullet Points: Using PowerPoint to tell a compelling story that gets results, "
                             "4th Edition", isbn="978-1-5093-0553-7")
    user1 = User(id=1, name="John Doe", email="johndoe@awsomejoe.com")

    book_circulations = [BookCirculation(book=book1, user=user1), BookCirculation(book=book2, user=user1)]

    email_sender = EmailSender()
    email_sender.notify_successful_book_borrows(book_circulations)