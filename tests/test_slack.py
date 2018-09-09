import unittest
from pusher.slack import PushSlack

class TestSlacker(unittest.TestCase):
    def setUp(self):
        self.pusher = PushSlack()

    def tearDown(self):
        pass

    def test_send_message(self):
        self.pusher.send_message("#test", "This is the 테스트 msg")

if __name__ == "__main__":
    unittest.main()