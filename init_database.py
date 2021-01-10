import re

import jieba
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine, PrimaryKeyConstraint, Text, DateTime, \
    Boolean, LargeBinary
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
import sqlite3 as sqlite
import random
import base64
import simplejson as json
import jieba.analyse

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
    title = Column(String, nullable=False)
    author = Column(String)
    publisher = Column(String)
    original_title = Column(Text)
    translator = Column(Text)
    pub_year = Column(Text)
    pages = Column(Integer)
    original_price = Column(Integer)  # 原价
    currency_unit = Column(Text)
    binding = Column(Text)
    isbn = Column(Text)
    author_intro = Column(Text)
    book_intro = Column(String)
    content = Column(Text)
    tags = Column(String)
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


# 搜索标题表
class Search_title(Base):
    __tablename__ = 'search_title'
    search_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), nullable=False)


# 搜索标签表
class Search_tags(Base):
    __tablename__ = 'search_tags'
    search_id = Column(Integer, primary_key=True, nullable=False)
    tags = Column(String, primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), nullable=False)


# 搜索作者表
class Search_author(Base):
    __tablename__ = 'search_author'
    search_id = Column(Integer, primary_key=True, nullable=False)
    author = Column(String, primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), nullable=False)


# 搜索书本内容表
class Search_book_intro(Base):
    __tablename__ = 'search_book_intro'
    search_id = Column(Integer, primary_key=True, nullable=False)
    book_intro = Column(String, primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), nullable=False)


class Bookinit:
    id: str
    title: str
    author: str
    publisher: str
    original_title: str
    translator: str
    pub_year: str
    pages: int
    price: int
    binding: str
    isbn: str
    author_intro: str
    book_intro: str
    content: str
    tags: [str]
    pictures: [bytes]

    def __init__(self):
        self.tags = []
        self.pictures = []


class BookDB:
    def __init__(self, large: bool = False):
        parent_path = os.path.dirname(os.path.dirname(__file__))
        self.db_s = os.path.join(parent_path, "D:\\fileneed\\DatabaseManagementSystem\\bookstore\\fe\\data\\book.db")
        self.db_l = os.path.join(parent_path, "fe/data/book_lx.db")
        if large:
            self.book_db = self.db_l
        else:
            self.book_db = self.db_s

    def get_book_count(self):
        conn = sqlite.connect(self.book_db)
        cursor = conn.execute(
            "SELECT count(id) FROM book")
        row = cursor.fetchone()
        return row[0]

    def get_book_info(self, start, size) -> [Book]:
        books = []
        conn = sqlite.connect(self.book_db)
        cursor = conn.execute(
            "SELECT id, title, author, "
            "publisher, original_title, "
            "translator, pub_year, pages, "
            "price, currency_unit, binding, "
            "isbn, author_intro, book_intro, "
            "content, tags, picture FROM book ORDER BY id "
            "LIMIT ? OFFSET ?", (size, start))
        for row in cursor:
            book = Bookinit()
            book.id = row[0]
            book.title = row[1]
            book.author = row[2]
            book.publisher = row[3]
            book.original_title = row[4]
            book.translator = row[5]
            book.pub_year = row[6]
            book.pages = row[7]
            book.price = row[8]
            book.currency_unit = row[9]
            book.binding = row[10]
            book.isbn = row[11]
            book.author_intro = row[12]
            book.book_intro = row[13]
            book.content = row[14]
            tags = row[15]
            picture = row[16]

            for tag in tags.split("\n"):
                if tag.strip() != "":
                    book.tags.append(tag)
            for i in range(0, random.randint(0, 9)):
                if picture is not None:
                    encode_str = base64.b64encode(picture).decode('utf-8')
                    book.pictures.append(encode_str)
            books.append(book)
        return books

    def send_info_to_db(self, start, size):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        conn = sqlite.connect(self.book_db)
        cursor = conn.execute(
            "SELECT id, title, author, "
            "publisher, original_title, "
            "translator, pub_year, pages, "
            "price, currency_unit, binding, "
            "isbn, author_intro, book_intro, "
            "content, tags, picture FROM book ORDER BY id "
            "LIMIT ? OFFSET ?", (size, start))
        for row in cursor:
            book = Book()
            book.book_id = row[0]
            book.title = row[1]
            book.author = row[2]
            book.publisher = row[3]
            book.original_title = row[4]
            book.translator = row[5]
            book.pub_year = row[6]
            book.pages = row[7]
            book.original_price = row[8]

            book.currency_unit = row[9]
            book.binding = row[10]
            book.isbn = row[11]
            book.author_intro = row[12]
            book.book_intro = row[13]
            book.content = row[14]
            tags = row[15]

            picture = row[16]
            # tagenum=MyEnum(enum.Enum)
            thelist = []  # 由于没有列表类型，故使用将列表转为text的办法
            for tag in tags.split("\n"):
                if tag.strip() != "":
                    # book.tags.append(tag)
                    thelist.append(tag)
            book.tags = str(thelist)  # 解析成list请使用eval()
            book.picture = None
            if picture is not None:
                book.picture = picture

            session.add(book)
        session.commit()
        # 关闭session
        session.close()

    def send_info(self):
        bookdb.send_info_to_db(0, bookdb.get_book_count())  # count=100 or 整张表


def insert_tags():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    row = session.execute("SELECT book_id,tags FROM book;").fetchall()
    print(row[1])
    m = 0
    for i in row[1:]:
        tmp = i.tags.replace("'", "").replace("[", "").replace("]",
                                                               "").split(", ")
        for j in tmp:
            session.execute(
                "INSERT into search_tags(search_id, tags, book_id) VALUES (%d, '%s', %d)"
                % (m, j, int(i.book_id)))
            m = m + 1
    session.commit()


def insert_author():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # Base.metadata.create_all(engine)
    row = session.execute("SELECT book_id, author FROM book;").fetchall()
    m = 0
    for i in row:
        tmp = i.author
        if tmp == None:
            j = '作者不详'
            session.execute(
                "INSERT into search_author(search_id, author, book_id) VALUES (%d, '%s', %d)"
                % (m, j, int(i.book_id)))
            m = m + 1
        else:
            tmp = re.sub(r'[\(\[\{（【][^)）】]*[\)\]\{\】\）]\s?', '', tmp)
            tmp = re.sub(r'[^\w\s]', '', tmp)
            length = len(tmp)
            for k in range(1, length + 1):
                if tmp[k - 1] == '':
                    continue
                j = tmp[:k]
                session.execute(
                    "INSERT into search_author(search_id, author, book_id) VALUES (%d, '%s', %d)"
                    % (m, j, int(i.book_id)))
                m = m + 1
    session.commit()


def insert_title():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # Base.metadata.create_all(engine)
    row = session.execute("SELECT book_id, title FROM book;").fetchall()
    m = 0
    for i in row:
        tmp = i.title
        # print(tmp)
        tmp = re.sub(r'[\(\[\{（【][^)）】]*[\)\]\{\】\）]\s?', '', tmp)
        tmp = re.sub(r'[^\w\s]', '', tmp)
        # 处理空标题
        if len(tmp) == 0:
            continue

        # 搜索引擎模式，在精确模式的基础上，对长词再次切分，提高召回率，适合用于搜索引擎分词。
        seg_list = jieba.cut_for_search(tmp)
        sig_list = []
        tag = 0
        for k in seg_list:
            sig_list.append(k)
            if k == tmp:
                tag = 1
        if tag == 0:
            sig_list.append(tmp)

        for j in sig_list:
            if j == "" or j == " ":
                continue
            session.execute(
                "INSERT into search_title(search_id, title, book_id) VALUES (%d, '%s', %d)"
                % (m, j, int(i.book_id)))
            m = m + 1
    session.commit()


def insert_book_intro():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # Base.metadata.create_all(engine)
    row = session.execute("SELECT book_id, book_intro FROM book;").fetchall()
    m = 0
    for i in row:
        tmp = i.book_intro
        if tmp != None:
            # print(tmp)
            # 采用textrank进行分词
            keywords_textrank = jieba.analyse.textrank(tmp)
            # print(keywords_textrank)
            # keywords_tfidf = jieba.analyse.extract_tags(tmp)
            # print(keywords_tfidf)
            for j in keywords_textrank:
                session.execute(
                    "INSERT into search_book_intro(search_id, book_intro, book_id) VALUES (%d, '%s', %d)"
                    % (m, j, int(i.book_id)))
                m = m + 1
    session.commit()


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
    Book1 = Book(book_id='1',
                 title='数据结构')
    Book2 = Book(book_id='2',
                 title='PRML')
    session.add_all([A_Store1, A_Store2, Book1, Book2])
    session.commit()

    StoreA = Store_detail(store_id='王掌柜的书店',
                          book_id='1',
                          stock_level=10,
                          price=1000)  # 价格单位是分
    StoreB = Store_detail(store_id='王掌柜的书店',
                          book_id='2',
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
    bookdb = BookDB(large=False)
    bookdb.send_info()
    insert_tags()
    insert_author()
    insert_title()
    insert_book_intro()
    add_info()
