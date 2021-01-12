import uuid

import jwt
import logging
import time
import sqlalchemy
from be.model import error
from be.db_conn import *


# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal},
        key=user_id,
        algorithm="HS256",
    )
    return encoded


# decode a JWT to a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }
def jwt_decode(encoded_token, user_id: str) -> str:
    decoded = jwt.decode(encoded_token, key=user_id, algorithms="HS256")
    return decoded


class Player():
    token_lifetime: int = 3600  # 3600 second

    def register(self, user_id: str, password: str):
        terminal = "terminal_{}".format(str(uuid.uuid1()))
        token = jwt_encode(user_id, terminal)
        cursor = session.query(User).filter(User.user_id == user_id).first()
        if cursor is not None:
            return error.error_exist_user_id(user_id)
        user_one = User(
            user_id=user_id,
            password=password,
            balance=0,
            token=token,
            terminal=terminal
        )
        session.add(user_one)
        session.commit()
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> (int, str):
        cursor = session.query(User).filter(User.user_id == user_id).first()
        if cursor is None:
            return error.error_authorization_fail()
        db_token = cursor.token
        print('sss')
        hex_str = r"\x" + bytes(token, encoding='utf-8').hex()
        if db_token != token and db_token != hex_str:
            return error.error_authorization_fail()
        return 200, "ok"

    def check_password(self, user_id: str, password: str) -> (int, str):
        user_one = session.query(User).filter(User.user_id == user_id).first()
        if user_one is None:
            return error.error_authorization_fail()

        if password != user_one.password:
            return error.error_authorization_fail()

        return 200, "ok"

    def login(self, user_id: str, password: str, terminal: str) -> (int, str, str):
        token = ""
        code, message = self.check_password(user_id, password)
        if code != 200:
            return code, message, ""
        token = jwt_encode(user_id, terminal)
        cursor = session.query(User).filter(User.user_id == user_id).first()
        cursor.token = token
        cursor.terminal = terminal
        session.commit()
        return 200, "ok", token

    def logout(self, user_id: str, token: str) -> bool:
        code, message = self.check_token(user_id, token)
        if code != 200:
            return code, message

        terminal = "terminal_{}".format(str(uuid.uuid1()))
        dummy_token = jwt_encode(user_id, terminal)
        cursor = session.query(User).filter(User.user_id == user_id).first()
        cursor.token = dummy_token
        cursor.terminal = terminal
        session.commit()
        return 200, "ok"

    def unregister(self, user_id: str, password: str) -> (int, str):
        code, message = self.check_password(user_id, password)
        if code != 200:
            return code, message
        cursor = session.query(User).filter(User.user_id == user_id).first()
        session.delete(cursor)
        session.commit()
        return 200, "ok"

    def change_password(self, user_id: str, old_password: str, new_password: str) -> bool:
        code, message = self.check_password(user_id, old_password)
        if code != 200:
            return code, message

        terminal = "terminal_{}".format(str(uuid.uuid1()))
        token = jwt_encode(user_id, terminal)
        cursor = session.query(User).filter(User.user_id == user_id).first()
        cursor.password = new_password
        cursor.token = token
        cursor.terminal = terminal
        session.commit()
        return 200, "ok"

    def search_author(self, author: str, page: int) -> (int, [dict]):  # 200,'ok',list[{str,str,str,str,list,bytes}]
        ret = []
        if page < 1:
            return 200, []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_author where author='%s') LIMIT 10 OFFSET %d" % (
                author, 10 * page - 10)).fetchall()
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author_ = record[1]
                publisher = record[2]
                book_intro = record[3]
                tags = record[4]
                ret.append(
                    {'title': title, 'author': author_, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags})
            return 200, ret
        else:
            return 200, []

    def search_book_intro(self, book_intro: str, page: int) -> (int, [dict]):
        ret = []
        if page < 1:
            return 200, []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_book_intro where book_intro='%s') LIMIT 10 OFFSET %d" % (
                book_intro, 10 * page - 10)).fetchall()  # 约对"小说"约0.09s
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author = record[1]
                publisher = record[2]
                book_intro_ = record[3]
                tags = record[4]
                ret.append(
                    {'title': title, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro_,
                     'tags': tags})
            return 200, ret
        else:
            return 200, []

    def search_tags(self, tags: str, page: int) -> (int, [dict]):
        ret = []
        if page < 1:
            return 200, []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_tags where tags='%s') LIMIT 10 OFFSET %d" % (
                tags, 10 * page - 10)).fetchall()
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author = record[1]
                publisher = record[2]
                book_intro = record[3]
                tags_ = record[4]
                ret.append(
                    {'title': title, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags_})
            return 200, ret
        else:
            return 200, []

    def search_title(self, title: str, page: int) -> (int, [dict]):
        ret = []
        if page < 1:
            return 200, []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_title where title='%s') LIMIT 10 OFFSET %d" % (
                title, 10 * page - 10)).fetchall()
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title_ = record[0]
                author = record[1]
                publisher = record[2]
                book_intro = record[3]
                tags = record[4]
                ret.append(
                    {'title': title_, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags})
            return 200, ret
        else:
            return 200, []

    def search_author_in_store(self, author: str, store_id: str, page: int) -> (int, [dict]):
        ret = []
        if page < 1:
            return 200, []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_author where author='%s') and "
            "book_id in (select book_id from store_detail where store_id='%s') LIMIT 10 OFFSET %d"
            % (author, store_id, 10 * page - 10)).fetchall()
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author_ = record[1]
                publisher = record[2]
                book_intro = record[3]
                tags = record[4]
                ret.append(
                    {'title': title, 'author': author_, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags})
            return 200, ret
        else:
            return 200, []

    def search_book_intro_in_store(self, book_intro: str, store_id: str, page: int) -> (int, [dict]):
        ret = []
        if page < 1:
            return 200, []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_book_intro where book_intro='%s') and "
            "book_id in (select book_id from store_detail where store_id='%s') LIMIT 10 OFFSET %d"
            % (book_intro, store_id, 10 * page - 10)).fetchall()
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author = record[1]
                publisher = record[2]
                book_intro_ = record[3]
                tags = record[4]
                ret.append(
                    {'title': title, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro_,
                     'tags': tags})
            return 200, ret
        else:
            return 200, []

    def search_tags_in_store(self, tags: str, store_id: str, page: int) -> (int, [dict]):
        ret = []
        if page < 1:
            return 200, []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_tags where tags='%s') and "
            "book_id in (select book_id from store_detail where store_id='%s') LIMIT 10 OFFSET %d"
            % (tags, store_id, 10 * page - 10)).fetchall()
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title = record[0]
                author = record[1]
                publisher = record[2]
                book_intro = record[3]
                tags_ = record[4]
                ret.append(
                    {'title': title, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags_})
            return 200, ret
        else:
            return 200, []

    def search_title_in_store(self, title: str, store_id: str, page: int) -> (int, [dict]):
        ret = []
        if page < 1:
            return 200, []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_title where title='%s') and "
            "book_id in (select book_id from store_detail where store_id='%s') LIMIT 10 OFFSET %d"
            % (title, store_id, 10 * page - 10)).fetchall()
        if len(records) != 0:
            for i in range(len(records)):
                record = records[i]
                title_ = record[0]
                author = record[1]
                publisher = record[2]
                book_intro = record[3]
                tags = record[4]
                ret.append(
                    {'title': title_, 'author': author, 'publisher': publisher,
                     'book_intro': book_intro,
                     'tags': tags})
            return 200, ret
        else:
            return 200, []
