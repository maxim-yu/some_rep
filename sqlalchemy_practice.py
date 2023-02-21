import sqlalchemy
from sqlalchemy.orm import sessionmaker
import json
from models import create_table, Publisher, Book, Shop, Stock, Sale
import os


def get_id():
    value = input("Введите ID или название издательства: ")
    try:
        value = int(value)
        print(f'Книги издательства с ID = {value}, продаются в следующих магазинах: ')
    except ValueError:
        print(f'Книги издательства {value}, продаются в следующих магазинах: ')
        value = int(session.query(Publisher.id).filter(Publisher.name == value).first()[0])
    return value


print("Для подключения к БД PostgreSQL, введите информацию: ")

database = os.getenv('database', default=input("Enter database: "))
user = os.getenv('user', default=input("Enter user: "))
password = os.getenv('password', default=input("Enter password: "))

DSN = f'postgresql://{user}:{password}@localhost:5432/{database}'

engine = sqlalchemy.create_engine(DSN)
create_table(engine)

Session = sessionmaker(bind=engine)
session = Session()


with open('test_data.json') as db:
    data = json.load(db)

for line in data:
    table_name = {
        'publisher': Publisher,
        'shop': Shop,
        'book': Book,
        'stock': Stock,
        'sale': Sale,
    }[line.get('model')]
    session.add(table_name(id=line.get('pk'), **line.get('fields')))
session.commit()

sample_request = session.query(Shop.name).join(Stock.shop).join(Book).join(Publisher).\
    filter(Stock.count > 0, Publisher.id == get_id()).all()

for shop in set(sample_request):
    print(*shop)

session.close()
