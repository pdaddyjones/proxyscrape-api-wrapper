""" proxyscrape client tests """
import unittest
from unittest.mock import patch, Mock
from proxyscrape.client import ProxyScrape

TEST_API_KEY = '1234567'
TEST_PROXY_LIST = ['127.0.0.1:80']


class TestHttpClient(unittest.TestCase):
    """  Proxyscrape test class """
    def setUp(self) -> None:
        self.client1 = ProxyScrape(TEST_API_KEY)
        self.client2 = ProxyScrape(TEST_API_KEY)
        self.client3 = ProxyScrape(TEST_API_KEY)

    @patch('proxyscrape.client.requests.get')
    def test_get_proxy_list(self, mock_get):
        mock_get.return_value = Mock(ok=True)
        mock_get.return_value.text = ' '.join(TEST_PROXY_LIST)

        proxy_list = self.client1.get_proxy_list()
        self.assertEqual(proxy_list, TEST_PROXY_LIST)

    @patch('proxyscrape.client.requests.get')
    def test_shared_proxy_list(self, mock_get):
        mock_get.return_value = Mock(ok=True)

        mock_get.return_value.text = ' '.join(TEST_PROXY_LIST)

        self.assertEqual(self.client1.proxy, self.client2.proxy)
        self.assertEqual(self.client3.next_proxy(), self.client1.proxy)

