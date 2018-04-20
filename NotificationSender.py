from model import BookCirculation
from playhouse.shortcuts import model_to_dict
from smtplib import SMTP
from email.message import EmailMessage

class NotificationSender:
    def send(self):
        pass

    def compose(self, book_to_return):
        pass


class EmailSender:
    def __init__(self):
        self.smtp = SMTP(host='smtp.mailtrap.io', port=2525)
        self.smtp.login('3f534eda171e91', '3ab5f8fea23d28')

    def send(self):
        query = BookCirculation.select().group_by(BookCirculation.user).\
            having((BookCirculation.user.email is not None) | (BookCirculation.return_time is None))

        for book_circulation in query:
            msg = self.compose(book_circulation)

            self.smtp.send_message(msg)

    def compose(self, book_to_return):
        msg = EmailMessage()
        msg.set_content("Bitch, you have books that you have not returned.")
        msg['Subject'] = "Sup"
        msg['From'] = "noreply@smartlib.com"
        msg['To'] = book_to_return.user.email

        return msg

    def __del__(self):
        self.smtp.close()

if __name__ == '__main__':
    email_sender = EmailSender()
    email_sender.send()