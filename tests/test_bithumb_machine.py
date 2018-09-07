import unittest
from machine.bithumb_machine import BithumbMachine
import inspect


class BithumbMachineTestCase(unittest.TestCase):

    def setUp(self):
        self.bithumb_machine = BithumbMachine()

    def tearDown(self):
        pass

    def test_get_ticker(self):
        print(inspect.stack()[0][3])
        ticker = self.bithumb_machine.get_ticker("ETC")
        assert ticker
        print(ticker)

    def test_get_filled_orders(self):
        print(inspect.stack()[0][3])
        ticker = self.bithumb_machine.get_filled_orders("ETC")
        assert ticker
        print(ticker)

    # def test_get_wallet_status(self):
    #     print(inspect.stack()[0][3])
    #     result = self.bithumb_machine.get_wallet_status("ETH")
    #     assert result
    #     print(result)
