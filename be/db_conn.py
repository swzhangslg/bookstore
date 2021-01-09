from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint, Text, DateTime, \
    Boolean, LargeBinary
from sqlalchemy.orm import sessionmaker
from datetime import datetime, time

Base = declarative_base()
engine = create_engine('postgresql://postgres:111016@localhost:5432/bookstore')
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
# 0为已付款，1为已发货，2为已收货, 3为已下单未付款,4为交易关闭

# 订单详情————同一家所有不同商品归为一个order
class Order_detail(Base):
    __tablename__ = 'order_detail'
    order_id = Column(String(1280), primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), primary_key=True, nullable=False)
    count = Column(Integer, nullable=False)


def user_id_exist(user_id):
    cursor = session.query(User).filter(User.user_id == user_id).first()
    if (cursor is None):
        return False
    else:
        return True

# 查询书店是否有某类书
def book_id_exist(store_id, book_id):
    cursor = session.query(Store_detail).filter(Store_detail.store_id == store_id, Store_detail.book_id == book_id).first()
    if (cursor is None):
        return False
    else:
        return True

def store_id_exist(store_id):
    cursor = session.query(Store).filter(Store.store_id == store_id).first()
    if (cursor is None):
        return False
    else:
        return True