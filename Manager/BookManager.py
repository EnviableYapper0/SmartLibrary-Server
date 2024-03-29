from Manager.DatabaseManager import DatabaseManager
from model import Book


class BookManager(DatabaseManager):
    def __init__(self):
        DatabaseManager.__init__(self)
        Book.create_table()

    def get_all_books(self):
        return DatabaseManager.get_list(
            Book.select().where(Book.is_available == True)
        )

    def add_book(self, json_data):
        return Book.create(**json_data)

    def get_book(self, book_id):
        return Book.get((Book.book_id == book_id) & (Book.is_available == True))

    def get_book_by_rfid(self, rfid):
        return Book.get((Book.rfid == rfid) & (Book.is_available == True))

    def mark_book_unavaliable(self, book_id):
        Book.set_by_id(book_id, {"is_available": False})

    def search(self, keyword):
        return DatabaseManager.get_list(
            Book.select().where((Book.title.contains(keyword)) & (Book.is_available == True))
        )

    def update_book_data(self, book_id, json_data):
        if 'book_id' in json_data.keys() and json_data['book_id'] != book_id:
            raise IndexError("Id mismatched.")

        row_changed = Book.set_by_id(book_id, json_data)
        return self.get_book(book_id)
