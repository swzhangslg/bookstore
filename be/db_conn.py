from init_database import *


def user_id_exist(user_id):
    cursor = session.query(User).filter(User.user_id == user_id).first()
    if (cursor is None):
        return False
    else:
        return True


# 查询书店是否有某类书
def book_id_exist(store_id, book_id):
    cursor = session.query(Store_detail).filter(Store_detail.store_id == store_id,
                                                Store_detail.book_id == book_id).first()
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
