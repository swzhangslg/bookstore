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
            print('db_token:',db_token)
            print(token)
            hex_str=r"\x"+bytes(token,encoding='utf-8').hex()
            print('hex_str:',hex_str)
            if db_token != token and db_token != hex_str:
                return False
            print('aaa')
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
            # print("xxx"+str(token))
            user_one = User(
                user_id=user_id,
                password=password,
                balance=0,
                token= token,
                terminal=terminal
            )
            session.add(user_one)
            session.commit()
        # except sqlite.Error:
        # return error.error_exist_user_id(user_id)
        # return 200, "ok"
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
        #token="1.1.1"
        #print("123"+str(token))
        cursor = session.query(User).filter(User.user_id == user_id).first()
        cursor.token = token
        cursor.terminal = terminal
        session.commit()
        # cursor = self.conn.execute(
        #     "UPDATE user set token= ? , terminal = ? where user_id = ?",
        #     (token, terminal, user_id), )
        # if cursor is None:
        #     return error.error_authorization_fail() + ("",)
        # self.conn.commit()
        # except sqlite.Error as e:
        #     return 200, "ok"
        # return 528, "{}".format(str(e)), ""
        # except BaseException as e:
        #     return 530, "{}".format(str(e)), ""
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
            # except sqlite.Error as e:
            # return 528, "{}".format(str(e))
            # return 200, "ok"
            # except BaseException as e:
            #     return 530, "{}".format(str(e))
            return 200, "ok"
        except sqlalchemy.exc.IntegrityError:
            return error.error_authorization_fail()

    def unregister(self, user_id: str, password: str) -> (int, str):
        code, message = self.check_password(user_id, password)
        if code != 200:
            return code, message
        cursor = session.query(User).filter(User.user_id == user_id).first()
        # self.session.delete(cursor)
        # cursor = self.conn.execute("DELETE from user where user_id=?", (user_id,))
        session.delete(cursor)
        session.commit()
        # return 528, "{}".format(str(e))
        # except BaseException as e:
        #     return 530, "{}".format(str(e))
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
        # cursor = self.conn.execute(
        #     "UPDATE user set password = ?, token= ? , terminal = ? where user_id = ?",
        #     (new_password, token, terminal, user_id), )
        return 200, "ok"
