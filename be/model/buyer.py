import uuid
import json
import logging
from datetime import datetime
from be.db_conn import user_id_exist,store_id_exist
from be.db_conn import session, Order,Store,Store_detail,Order_detail,User
from be.model import error


# class Buyer_func(DBConn):
#     def __init__(self):
#         DBConn.__init__(self)

#     # 检查未付款order是否超出15min
#     def check_order(self, order_id):
#         order = self.session.query(Order).filter(Order.order_id == order_id).first()
#         if order is not None:
#             if order.status == 3:
#                 paytime = order.paytime
#                 time_now = datetime.now()
#                 old_time = datetime.strptime(str(paytime), "%Y-%m-%d %H:%M:%S.%f")
#                 new_time = datetime.strptime(str(time_now), "%Y-%m-%d %H:%M:%S.%f")
#                 time_lag = (new_time - old_time).seconds  # 计算时间差

#                 # 超出15min未付款则关闭订单
#                 if (time_lag > 15 * 60):
#                     order.status = 4
#                     self.session.commit()


class Buyer():

    def new_order(self, user_id: str, store_id: str, id_and_count: [(str, int)]) -> (int, str, str):
        order_id = ""
        if not user_id_exist(user_id):
            return error.error_non_exist_user_id(user_id) + (order_id,)
        if not store_id_exist(store_id):
            return error.error_non_exist_store_id(store_id) + (order_id,)
        uid = "{}_{}_{}".format(user_id, store_id, str(uuid.uuid1()))

        for book_id, count in id_and_count:
            store_detail = session.query(Store_detail).filter(Store_detail.store_id == store_id,
                                                                    Store_detail.book_id == book_id).first()
            if (store_detail is None):
                return error.error_non_exist_book_id(book_id) + (order_id,)

            stock_level = store_detail.stock_level

            if stock_level < count:
                return error.error_stock_level_low(book_id) + (order_id,)

            store_detail.stock_level -= count
            session.commit()
            session.add(Order_detail(order_id=uid, book_id=book_id, count=count))
            session.commit()
        session.add(
            Order(order_id=uid, user_id=user_id, store_id=store_id, paytime=datetime.now(), status=3))
        session.commit()

        order_id = uid
        return 200, "ok", order_id

    def payment(self, user_id: str, password: str, order_id: str) -> (int, str):
        # Buyer_func.check_order(self, order_id)

        order = session.query(Order).filter(Order.order_id == order_id).first()

        if order is None:
            return error.error_invalid_order_id(order_id)
        if order.status == 4:
            return error.error_order_closed(order_id)
        elif order.status != 3:
            return error.error_order_has_been_paid(order_id)

        # order_id = order.order_id
        buyer_id = order.user_id
        store_id = order.store_id

        if buyer_id != user_id:
            return error.error_authorization_fail()

        buyer = session.query(User).filter(User.user_id == buyer_id).first()
        if buyer is None:
            return error.error_non_exist_user_id(buyer_id)
        balance = buyer.balance
        if (password != buyer.password):
            return error.error_authorization_fail()

        store = session.query(Store).filter(Store.store_id == store_id).first()
        if store is None:
            return error.error_non_exist_store_id(store_id)

        seller_id = store.user_id
        if not user_id_exist(seller_id):
            return error.error_non_exist_user_id(seller_id)

        order_detail = session.query(Order_detail).filter(Order_detail.order_id == order_id).all()
        total_price = 0
        for i in range(0,len(order_detail)):
            book_id = order_detail[i].book_id
            book = session.query(Store_detail).filter(Store_detail.store_id == store_id,
                                                            Store_detail.book_id == book_id).first()
            count = order_detail[i].count
            price = book.price
            total_price = total_price + price * count

        if balance < total_price:
            return error.error_not_sufficient_funds(order_id)

        buyer.balance -= total_price
        seller = session.query(User).filter(User.user_id == seller_id).first()
        seller.balance += total_price

        order.status = 0  # 设置付款状态：已支付
        order.paytime = datetime.now()
        # ?????代码在干嘛？ 删除订单？
        # cursor = conn.execute("DELETE FROM new_order WHERE order_id = ?", (order_id,))
        # if cursor.rowcount == 0:
        #     return error.error_invalid_order_id(order_id)
        #
        # cursor = conn.execute("DELETE FROM new_order_detail where order_id = ?", (order_id,))
        # if cursor.rowcount == 0:
        #     return error.error_invalid_order_id(order_id)
        session.commit()
        return 200, "ok"

    def add_funds(self, user_id, password, add_value) -> (int, str):
        user = session.query(User).filter(User.user_id == user_id).first()
        if user is None:
            return error.error_authorization_fail()

        if user.password != password:
            return error.error_authorization_fail()

        user.balance += add_value
        session.commit()
        return 200, "ok"

    def receive_books(self, buyer_id, order_id):
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if order is None:
            return error.error_invalid_order_id(order_id)
        if order.status ==0:
            return 522, "book hasn't been sent to costumer"
        if order.status ==2:
            return 523, "book has been received"
        # if order.status ==3: 已取消
        if order.user_id!= buyer_id:
            return error.error_authorization_fail()
        order.status =2
        session.commit()
        return 200, "ok"