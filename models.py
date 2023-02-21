from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import ForeignKey, Column, Integer, String, Numeric, DateTime


Base = declarative_base()


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True, nullable=False)


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    title = Column(String(length=50), nullable=False)
    id_publisher = Column(Integer, ForeignKey('publisher.id'), nullable=False)

    publishers = relationship(Publisher, backref='books')


class Shop(Base):
    __tablename__ = 'shop'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), unique=True, nullable=False)

    def __str__(self):
        return self.name


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer, primary_key=True)
    id_book = Column(Integer, ForeignKey('book.id'), nullable=False)
    id_shop = Column(Integer, ForeignKey('shop.id'), nullable=False)
    count = Column(Integer, nullable=False)

    book = relationship(Book, backref='books')
    shop = relationship(Shop, backref='shops')


class Sale(Base):
    __tablename__ = 'sale'

    id = Column(Integer, primary_key=True)
    price = Column(Numeric, nullable=False)
    date_sale = Column(DateTime, nullable=False)
    count = Column(Integer, nullable=False)
    id_stock = Column(Integer, ForeignKey('stock.id'), nullable=False)

    stock = relationship(Stock, backref='stocks')


def create_table(engine):
    Base.metadata.create_all(engine)
