from be.model import error
from be.db_conn import *
import json
from sqlalchemy import and_


class Seller():

    def add_book(self, user_id: str, store_id: str, book_id: str, book_json_str: str, stock_level: int):
        book_json = json.loads(book_json_str)
        if not user_id_exist(user_id):
            return error.error_non_exist_user_id(user_id)
        if not store_id_exist(store_id):
            return error.error_non_exist_store_id(store_id)
        if book_id_exist(store_id, book_id):
            return error.error_exist_book_id(book_id)
        book_one = Book(book_id = book_id,
                        title = book_json.get("title"),
                        author = book_json.get("author"),
                        publisher = book_json.get("publisher"),
                        original_title = book_json.get("original_title"),
                        translator = book_json.get("translator"),
                        pub_year = book_json.get("pub_year"),
                        pages = book_json.get("pages"),
                        original_price = book_json.get("price"),
                        currency_unit = book_json.get("currency_unit"),
                        binding = book_json.get("binding"),
                        isbn = book_json.get("isbn"),
                        author_intro = book_json.get("author_intro"),
                        book_intro = book_json.get("book_intro"),
                        content = book_json.get("content"),
                        tags = book_json.get("tags"),
                        picture = book_json.get("picture")
                        )
        if not session.query(Book).filter(Book.book_id==book_id).first():
            session.add(book_one)
            # session.commit()
        store_detail_one=Store_detail(
            store_id = store_id,
            book_id = book_id,
            stock_level = stock_level,
            price = book_json.get("price")
        )
        session.add(store_detail_one)
        session.commit()
        return 200, "ok"

    def add_stock_level(self, user_id: str, store_id: str, book_id: str, add_stock_level: int):
        if not user_id_exist(user_id):
            return error.error_non_exist_user_id(user_id)
        if not store_id_exist(store_id):
            return error.error_non_exist_store_id(store_id)
        if not book_id_exist(store_id, book_id):
            return error.error_non_exist_book_id(book_id)

        cursor = session.query(Store_detail).filter(
            and_(Store_detail.store_id == store_id, Store_detail.book_id == book_id)).first()
        cursor.stock_level = cursor.stock_level + add_stock_level
        session.commit()
        return 200, "ok"

    def create_store(self, user_id: str, store_id: str) -> (int, str):
        if not user_id_exist(user_id):
            return error.error_non_exist_user_id(user_id)
        if store_id_exist(store_id):
            return error.error_exist_store_id(store_id)
        store_one = Store(user_id=user_id, store_id=store_id)
        session.add(store_one)
        session.commit()
        return 200, "ok"


    def send_books(self,seller_id,order_id):
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if order is None:
            return error.error_invalid_order_id(order_id)
        if order.status !=0:
            return 521,'books has been sent to costumer or the order is cancelled'
        # status == 4
        store = session.query(Store).filter(Store.store_id == order.store_id).first()
        # 店铺主是不是seller
        if seller_id != store.user_id:
            return error.error_authorization_fail()
        order.status=1
        session.commit()
        return 200, "ok"