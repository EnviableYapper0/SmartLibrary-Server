from Manager.DatabaseManager import DatabaseManager
from model import Book


class BookManager(DatabaseManager):
    def __init__(self):
        DatabaseManager.__init__(self)
        Book.create_table()

    def get_all_books(self):
        book_list = []

        for book in Book.select():
            book_list.append(book)

        return book_list

    def add_book(self, json_data):
        return Book.create(**json_data)

    def get_book(self, book_id):
        return Book.get_by_id(book_id)

    def get_book_by_rfid(self, rfid):
        return Book.get(Book.rfid == rfid)

    def update_book_data(self, book_id, json_data):
        if 'book_id' in json_data.keys() and json_data['book_id'] != book_id:
            raise IndexError("Id mismatched.")

        row_changed = Book.set_by_id(book_id, json_data)
        return self.get_book(book_id)
