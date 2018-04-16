from peewee import *
from datetime import datetime
from Database import database


class BaseModel(Model):
    class Meta:
        database = database


class Book(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField()
    isbn = CharField(max_length=20)
    added_on = DateTimeField(default=datetime.now)
    rfid = CharField(null=True, default=None)
    is_available = BooleanField(default=True)


class User(BaseModel):
    id = AutoField(primary_key=True)
    name = TextField()
    registered_on = DateTimeField(default=datetime.now)
    rfid = CharField(null=True, default=None)
    is_active = BooleanField(default=True)


class BookCirculation(BaseModel):
    id = AutoField(primary_key=True)
    book = ForeignKeyField(Book, backref='circulation_history')
    user = ForeignKeyField(User, backref='borrow_history')
    borrow_time = DateTimeField(default=datetime.now)
    return_time = DateTimeField(null=True, default=None)

    def is_returned(self):
        return not self.borrow_time.is_null()