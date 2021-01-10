import jwt
import logging
import sqlite3 as sqlite
import time

import sqlalchemy

from be.model import error

from be.db_conn import session, User


# encode a json string like:
#   {
#       "user_id": [user name],
#       "terminal": [terminal code],
#       "timestamp": [ts]} to a JWT
#   }


def jwt_encode(user_id: str, terminal: str) -> str:
    encoded = jwt.encode(
        {"user_id": user_id, "terminal": terminal, "timestamp": time.time()},
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

    def __check_token(self, user_id, db_token, token) -> bool:
        try:
            hex_str=r"\x"+bytes(token,encoding='utf-8').hex()
            if db_token != token and db_token != hex_str:
                return False
            jwt_text = jwt_decode(encoded_token=token, user_id=user_id)
            ts = jwt_text["timestamp"]
            if ts is not None:
                now = time.time()
                if self.token_lifetime > now - ts >= 0:
                    return True
        except jwt.exceptions.InvalidSignatureError as e:
            logging.error(str(e))
            return False

    def register(self, user_id: str, password: str):
        try:
            terminal = "terminal_{}".format(str(time.time()))
            token = jwt_encode(user_id, terminal)
            user_one = User(
                user_id=user_id,
                password=password,
                balance=0,
                token= token,
                terminal=terminal
            )
            session.add(user_one)
            session.commit()
        except sqlalchemy.exc.IntegrityError:
            return error.error_exist_user_id(user_id)
        return 200, "ok"

    def check_token(self, user_id: str, token: str) -> (int, str):
        cursor = session.query(User).filter(User.user_id == user_id).first()
        if cursor is None:
            return error.error_authorization_fail()
        db_token = cursor.token
        print('sss')
        if not self.__check_token(user_id, db_token, token):
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
        try:
            code, message = self.check_token(user_id, token)
            if code != 200:
                return code, message

            terminal = "terminal_{}".format(str(time.time()))
            dummy_token = jwt_encode(user_id, terminal)
            cursor = session.query(User).filter(User.user_id == user_id).first()
            cursor.token = dummy_token
            cursor.terminal = terminal
            session.commit()
            return 200, "ok"
        except sqlalchemy.exc.IntegrityError:
            return error.error_authorization_fail()

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

        terminal = "terminal_{}".format(str(time.time()))
        token = jwt_encode(user_id, terminal)
        cursor = session.query(User).filter(User.user_id == user_id).first()
        cursor.password = new_password
        cursor.token = token
        cursor.terminal = terminal
        session.commit()
        return 200, "ok"


    def search_author(self, author: str) -> (int, [dict]):  # 200,'ok',list[{str,str,str,str,list,bytes}]
        ret = []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_author where author='%s')" % (
                author)).fetchall()
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

    def search_book_intro(self, book_intro: str) -> (int, [dict]):
        ret = []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_book_intro where book_intro='%s')" % (
                book_intro)).fetchall()  # 约对"小说"约0.09s
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

    def search_tags(self, tags: str) -> (int, [dict]):
        ret = []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_tags where tags='%s')" % (
                tags)).fetchall()
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

    def search_title(self, title: str) -> (int, [dict]):
        ret = []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_title where title='%s')" % (
                title)).fetchall()
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

    def search_author_in_store(self, author: str, store_id: str) -> (int, [dict]):
        ret = []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_author where author='%s') and "
            "book_id in (select book_id from store_detail where store_id='%s')"
            % (author, store_id)).fetchall()
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

    def search_book_intro_in_store(self, book_intro: str, store_id: str) -> (int, [dict]):
        ret = []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_book_intro where book_intro='%s') and "
            "book_id in (select book_id from store_detail where store_id='%s')"
            % (book_intro, store_id)).fetchall()
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

    def search_tags_in_store(self, tags: str, store_id: str) -> (int, [dict]):
        ret = []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_tags where tags='%s') and "
            "book_id in (select book_id from store_detail where store_id='%s')"
            % (tags, store_id)).fetchall()
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

    def search_title_in_store(self, title: str, store_id: str) -> (int, [dict]):
        ret = []
        records = session.execute(
            "SELECT title,author,publisher,book_intro,tags "
            "FROM book WHERE book_id in "
            "(select book_id from search_title where title='%s') and "
            "book_id in (select book_id from store_detail where store_id='%s')"
            % (title, store_id)).fetchall()
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

