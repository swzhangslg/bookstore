import pytest

from fe.access.buyer import Buyer
from fe.test.gen_book_data import GenBook
from fe.access.new_buyer import register_new_buyer
from fe.access.book import Book
import uuid
import random


class TestSearchOrder:
    @pytest.fixture(autouse=True)
    def pre_run_initialization(self):
        self.buyer_id = "test_search_order_buyer_id_{}".format(str(uuid.uuid1()))
        self.password = self.buyer_id
        b = register_new_buyer(self.buyer_id, self.password)
        self.buyer = b
        # code, self.order_id = b.new_order(self.store_id, buy_book_id_list)
        # assert code == 200
        # self.total_price = 0
        # for item in self.buy_book_info_list:
        #     book: Book = item[0]
        #     num = item[1]
        #     if book.price is None:
        #         continue
        #     else:
        #         self.total_price = self.total_price + book.price * num
        yield

    def test_ok(self):
        order_num = random.randint(1, 10)
        for i in range(order_num):
            self.seller_id = "test_search_order_seller_id_{}".format(str(uuid.uuid1()))
            self.store_id = "test_search_order_store_id_{}".format(str(uuid.uuid1()))
            self.gen_book = GenBook(self.seller_id, self.store_id)
            self.seller = self.gen_book.seller
            ok, buy_book_id_list = self.gen_book.gen(non_exist_book_id=False, low_stock_level=False, max_book_count=5)
            self.buy_book_info_list = self.gen_book.buy_book_info_list
            assert ok

            self.total_price = 0
            for item in self.buy_book_info_list:
                book: Book = item[0]
                num = item[1]
                self.total_price = self.total_price + book.price * num
            code = self.buyer.add_funds(self.total_price + 99999)
            assert code == 200
            code, self.order_id = self.buyer.new_order(self.store_id, buy_book_id_list)
            assert code == 200
            code = self.buyer.payment(self.store_id)
            assert code == 200
        code = self.buyer.search_order()
        assert code == 200

    # def close_paid(self):
    #     code = self.buyer.add_funds(self.total_price)
    #     assert code == 200
    #     code = self.buyer.payment(self.order_id)
    #     assert code == 200
    #     code = self.buyer.close_order(self.order_id)
    #     assert code == 200

    def test_authorization_error(self):
        self.buyer.password = self.buyer.password + "_x"
        code = self.buyer.search_order()
        assert code != 200

        self.buyer_id = self.buyer_id + "_x"
        code = self.buyer.search_order()
        assert code != 200

    def test_repeat_close(self):
        code = self.buyer.close_order(self.order_id)
        assert code == 200
        code = self.buyer.close_order(self.order_id)
        assert code != 200

    # def test_can_not_close(self):
    #     # 发货收货
    #     code = self.buyer.close_order(self.order_id)
    #     assert code != 200
