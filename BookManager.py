from model import Book


class BookManager(object):
    def __init__(self):
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
        if 'id' in json_data and json_data['id'] != book_id:
            raise IndexError("Id mismatched.")

        Book.update(**json_data).where(Book.id == book_id).execute()
        return self.get_book(book_id)