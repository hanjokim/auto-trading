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

    def test_get_wallet_status(self):
        print(inspect.stack()[0][3])
        result = self.coinone_machine.get_wallet_status()
        assert result
        print(result)