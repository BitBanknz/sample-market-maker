import unittest

from market_maker import bitbank


class MyTestCase(unittest.TestCase):
    def test_mode(self):
        bitbank.set_sell_mode(True)
        mode = bitbank.get_sell_mode()
        self.assertEqual(mode, True)
        bitbank.set_sell_mode(False)
        mode = bitbank.get_sell_mode()
        self.assertEqual(mode, False)

        bitbank.set_sell_mode(None)
        mode = bitbank.get_sell_mode()
        self.assertEqual(mode, None)


if __name__ == '__main__':
    unittest.main()
