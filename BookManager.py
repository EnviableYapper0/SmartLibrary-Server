from model import Book
from playhouse.shortcuts import model_to_dict


class BookManager(object):
    def get_all_books(self):
        book_list = []
        for book in Book.select():
            book_list.append(model_to_dict(book))

        return book_list

    def add_book(self, json_data):
        print(json_data)
        return model_to_dict(Book.create(**json_data))