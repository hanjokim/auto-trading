import unittest
from machine.coinone_machine import CoinOneMachine
import inspect


class CoinOneMachineTestCase(unittest.TestCase):
    def setUp(self):
        self.coinone_machine = CoinOneMachine()

    def tearDown(self):
        pass

    # def test_set_token(self):
    #     print(inspect.stack()[0][3])
    #     expire, access_token, refresh_token = self.coinone_machine.set_token()
    #     assert access_token
    #     print(expire, access_token, refresh_token)

    # def test_get_wallet_status(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.get_wallet_status()
    #     assert result
    #     print(result)

    # def test_buy_order(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.buy_order(currency_type="btc", price="230", qty="1", order_type="limit")
    #     assert result
    #     print(result)

    # def test_sell_coin_order(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.sell_order(currency_type="btc", price="230", qty="1", order_type="limit")
    #     assert result
    #     print(result)

    # def test_cancel_order(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.cancel_order(currency_type="btc", order_type="buy", order_id="")
    #     assert result
    #     print(result)

    # def test_get_list_my_orders(self):
    #     print(inspect.stack()[0][3])
    #     result = self.coinone_machine.get_list_my_orders(currency_type="btc")
    #     assert result
    #     print(result)

    def test_get_my_order_status(self):
        print(inspect.stack()[0][3])
        result = self.coinone_machine.get_my_order_status(currency_type="btc", order_id="")
        assert result
        print(result)