from model import Book
from Database import database


class BookManager(object):
    def __init__(self):
        database.connect()
        Book.create_table()

    def get_all_books(self):
        book_list = []

        for book in Book.select().where(Book.is_available == True):
            book_list.append(book)

        return book_list

    def add_book(self, json_data):
        return Book.create(**json_data)

    def get_book(self, book_id):
        return Book.get(Book.book_id == book_id and Book.is_available == True)

    def get_book_by_rfid(self, rfid):
        return Book.get(Book.rfid == rfid and Book.is_available == True)

    def update_book_data(self, book_id, json_data):
        if 'book_id' in json_data.keys() and json_data['book_id'] != book_id:
            raise IndexError("Id mismatched.")

        row_changed = Book.set_by_id(book_id, json_data)
        return self.get_book(book_id)

    def __del__(self):
        database.close()