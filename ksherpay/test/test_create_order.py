import unittest
from ksherpay import Payment
import os
import json
import logging
from dotenv import load_dotenv
import webbrowser
logging.root.setLevel('INFO')

class OrderCreateTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv()
        self.BASE_URL = 'https://dev.vip.ksher.net'
        self.token = os.environ.get("API_TOKEN") 
        logging.info("token:{}".format(self.token))
        # self.database_name = "trivia_test"
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        # setup_db(self.app, self.database_path)

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_success_create(self):
        payment_handle = Payment(base_url=self.BASE_URL, token=self.token)
        data = {
            "amount": 100,
            "channel_list": "linepay,airpay,wechat,bbl_promptpay,truemoney,ktbcard",
            "note": "string",
            "redirect_url": "http://www.baidu.com",
            "redirect_url_fail": "http://www.baidu.com",
            "signature": "string",
            "timestamp": "string"
        }
        data['merchant_order_id'] = payment_handle.order.generate_order_id()
        resp = payment_handle.order.create(data)
        self.assertEqual(resp.status_code, 200)
        if resp.status_code == 200:
            logging.info("successfully create order with following response data:")
            data = resp.json()
            logging.info(f"data:{data}")
            self.assertEqual(data['error_code'], 'SUCCESS')
            self.assertIn('gateway.ksher.com',data['reference'])
    
    def test_fail_create(self):
        payment_handle = Payment(base_url=self.BASE_URL, token=self.token)
        # try missing some paramenter
        data = {
            "note": "string",
            "redirect_url": "http://www.baidu.com",
            "redirect_url_fail": "http://www.baidu.com",
            "signature": "string",
            "timestamp": "string"
        }
        data['merchant_order_id'] = payment_handle.order.generate_order_id()
        resp = payment_handle.order.create(data)
        self.assertEqual(resp.status_code, 400)

    # def test_create_query_pending(self):
    #     # ceate an order and not pay result in pending order
    #     payment_handle = Payment(base_url=self.BASE_URL, token=self.token)
    #     data = {
    #         "amount": 100,
    #         "channel_list": "linepay,airpay,wechat,bbl_promptpay,truemoney,ktbcard",
    #         "note": "string",
    #         "redirect_url": "http://www.baidu.com",
    #         "redirect_url_fail": "http://www.baidu.com",
    #         "signature": "string",
    #         "timestamp": "string"
    #     }
    #     data['merchant_order_id'] = payment_handle.order.generate_order_id()
    #     resp = payment_handle.order.create(data)
    #     self.assertEqual(resp.status_code, 200)
    #     if resp.status_code == 200:
    #         logging.info("successfully create order with following response data:")
    #         data = resp.json()
    #         logging.info(f"data:{data}")
    #         self.assertEqual(data['error_code'], 'SUCCESS')
    #         self.assertIn('gateway.ksher.com',data['reference'])

    #         resp = payment_handle.order.query(data['merchant_order_id'])
    #         self.assertEqual(resp.status_code, 200)
    #         logging.info(f"data:{data}")

        

        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()