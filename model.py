from peewee import *
from datetime import datetime, timedelta
from Database import database


class BaseModel(Model):
    class Meta:
        database = database


class Book(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    name = TextField()
    isbn = CharField(max_length=20, unique=True)
    added_on = DateTimeField(default=datetime.now)
    rfid = CharField(null=True, default=None, unique=True)
    is_available = BooleanField(default=True)


class User(BaseModel):
    id = AutoField(primary_key=True, unique=True)
    name = TextField()
    registered_on = DateTimeField(default=datetime.now)
    line_token = CharField(null=True, default=None)
    rfid = CharField(null=True, default=None, unique=True)
    email = CharField(null=True, default=None)
    is_active = BooleanField(default=True)


# Workaround: BookCirculations due_time cannot detect the function if its part of itself
def default_return_time():
    return BookCirculation.default_return_time()


class BookCirculation(BaseModel):
    id = AutoField(primary_key=True)
    book = ForeignKeyField(Book, backref='circulation_history')
    user = ForeignKeyField(User, backref='borrow_history')
    borrow_time = DateTimeField(null=False, default=datetime.now)
    due_time = DateTimeField(null=False, default=default_return_time)
    return_time = DateTimeField(null=True, default=None)

    def is_returned(self):
        return not self.borrow_time.is_null()

    @staticmethod
    def default_return_time():
        return datetime.now() + timedelta(days=7)
