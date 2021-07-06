import os

DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

connection =  f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'

test_connection = f'sqlite:///{DB_NAME}.db'

