import unittest2
from unittest2 import SkipTest
import json

import btctradeapi
from btctradeapi.private import PrivateAPI
from btctradeapi.deals import DEALS


class TestPrivateAPI(unittest2.TestCase):

    @classmethod
    def setUpClass(cls):
        json_data = json.load(open('test/keys.sec'))
        cls.api = PrivateAPI(json_data['pubkey'], json_data['privkey'])

    def test_auth(self):
        auth_result = self.api.auth()
        self.assertEqual(auth_result['status'], True)
        self.assertEqual(auth_result['public_key'], self.api.pubkey)

    def test_balance(self):
        balance_result = self.api.balance()
        self.assertIn('msg_count', balance_result.keys())
        self.assertIn('accounts', balance_result.keys())

    #@unittest2.skip('waiting for answer in support')
    def test_sell(self):
        sell_uah_to_doge = self.api.sell(currency_from='UAH', currency_to='DOGE', count=10, price=0.0051)
        print sell_uah_to_doge
        self.assertTrue((sell_uah_to_doge['status'] == "processed") or (sell_uah_to_doge['status'] is True))

    def test_buy(self):
        buy_doge_with_uah = self.api.buy(currency_from='UAH', currency_to='DOGE', count=10, price=0.0056)
        self.assertTrue((buy_doge_with_uah['status'] == "processed") or (buy_doge_with_uah['status'] is True))

    def test_opened_orders(self):
        doge_uah_opened_orders_list = self.api.opened_orders('doge_uah')
        self.assertIsInstance(doge_uah_opened_orders_list['your_open_orders'], list)

    def test_order_status(self):
        order_status = self.api.order_status(1)
        self.assertIn('status', order_status.keys())

    #@unittest2.skip('waiting for answer in support')
    def test_remove_order(self):
        sell_uah_to_doge = self.api.sell(currency_from='UAH', currency_to='DOGE', count=10, price=0.0051)
        orders_list = self.api.opened_orders('doge_uah')
        self.assertTrue((sell_uah_to_doge['status'] == "processed") or (sell_uah_to_doge['status'] is True))
        print sell_uah_to_doge
        remove_order = self.api.remove_order(orders_list["your_open_orders"][0]["id"])
        self.assertIn('status', remove_order.keys())

    def test_get_cost_of_buying(self):
        cost_of_buying_btc = self.api.get_cost_of_buying(DEALS.btc_uah, amount=1)
        self.assertEqual(cost_of_buying_btc['status'], True)

    def test_get_cost_of_selling(self):
        cost_of_selling_btc = self.api.get_cost_of_selling(DEALS.btc_uah, amount=1)
        self.assertEqual(cost_of_selling_btc['status'], True)

