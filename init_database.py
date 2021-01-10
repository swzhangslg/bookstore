from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint, Text, DateTime, \
    Boolean, LargeBinary
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()
engine = create_engine('postgresql://postgres:811157@localhost:5432/bookstore')
DBSession = sessionmaker(bind=engine)
session = DBSession()


# 用户表
class User(Base):
    __tablename__ = 'user'
    user_id = Column(String(128), primary_key=True)
    password = Column(String(128), nullable=False)
    balance = Column(Integer, nullable=False)
    token = Column(String(4000), nullable=False)
    terminal = Column(String(256), nullable=False)


# 商店表（含书本信息）
class Store(Base):
    __tablename__ = 'store'
    store_id = Column(String(128), primary_key=True)
    user_id = Column(String(128), ForeignKey('user.user_id'), nullable=False)


# 商店详情表
class Store_detail(Base):
    __tablename__ = 'store_detail'
    store_id = Column(String(128), ForeignKey('store.store_id'), primary_key=True)
    book_id = Column(String(128), ForeignKey('book.book_id'), primary_key=True)
    stock_level = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)  # 售价


class Book(Base):
    __tablename__ = 'book'
    book_id = Column(String(128), primary_key=True)
    title = Column(Text, nullable=False)
    author = Column(Text)
    publisher = Column(Text)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    original_price = Column(Integer)  # 原价
    currency_unit = Column(Text)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(Text)
    content = Column(Text)
    tags = Column(Text)
    picture = Column(LargeBinary)


class Order(Base):
    __tablename__ = 'order'
    order_id = Column(String(1280), primary_key=True)
    user_id = Column(String(128), ForeignKey('user.user_id'), nullable=False)
    store_id = Column(String(128), ForeignKey('store.store_id'), nullable=False)
    paytime = Column(DateTime, nullable=True)
    status = Column(Integer(), nullable=True)  # 0为已付款，1为已发货，2为已收货, 3为已下单未付款


# 订单详情————同一家所有不同商品归为一个order
class Order_detail(Base):
    __tablename__ = 'order_detail'
    order_id = Column(String(1280), primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), primary_key=True, nullable=False)
    count = Column(Integer, nullable=False)


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)


def add_info():
    A = User(user_id='王掌柜',
             password='123456',
             balance=100,
             token='***',
             terminal='Edge')
    B = User(user_id='小明',
             password='123456',
             balance=500,
             token='***',
             terminal='Chrome')
    session.add_all([A, B])
    session.commit()

    A_Store1 = Store(user_id='王掌柜',
                     store_id='王掌柜的书店')
    A_Store2 = Store(user_id='王掌柜',
                     store_id='王掌柜的进口书店')
    Book1 = Book(book_id='1000067',
                 title='数据结构')
    Book2 = Book(book_id='1000134',
                 title='PRML')
    session.add_all([A_Store1, A_Store2, Book1, Book2])
    session.commit()

    StoreA = Store_detail(store_id='王掌柜的书店',
                          book_id='1000067',
                          stock_level=10,
                          price=1000)  # 价格单位是分
    StoreB = Store_detail(store_id='王掌柜的书店',
                          book_id='1000134',
                          stock_level=10,
                          price=10000)
    session.add_all([StoreA, StoreB])
    session.commit()

    # OrderA = Order(order_id='order1',
    #                user_id='小明',
    #                store_id='王掌柜的书店',
    #                paytime=datetime.now(),
    #                status=0)
    # OrderB = Order(order_id='order2',
    #                user_id='小明',
    #                store_id='王掌柜的进口书店',
    #                paytime=datetime.now(),
    #                status=3)
    # session.add_all([OrderA, OrderB])
    # session.commit()

    # Order_detailA = Order_detail(order_id='order1',
    #                              book_id='1',
    #                              count=2)
    # Order_detailB = Order_detail(order_id='order2',
    #                              book_id='2',
    #                              count=1)
    # session.add_all([Order_detailA, Order_detailB])
    # session.commit()
    # 关闭session
    session.close()


if __name__ == "__main__":
    drop_db()
    init_db()
    add_info()
