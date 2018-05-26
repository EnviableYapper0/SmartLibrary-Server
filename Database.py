from peewee import PostgresqlDatabase
import os

db_user = os.environ["DB_USER"]
db_pass = os.environ["DB_PASS"]
db_host = os.environ["DB_HOST"]


database = PostgresqlDatabase("SmartLib", user=db_user, password=db_pass, host=db_host)
