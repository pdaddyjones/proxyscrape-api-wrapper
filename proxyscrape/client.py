""" API Wrapper for Proxyscrape """
import re
import requests
from tinydb import TinyDB, Query
from tinydb.operations import increment, set


class ProxyScrape:
    """ Base class to get proxyscrape proxies """

    def __init__(self, api_key: str, cyclic: bool = False, storage_path: str = 'proxyscrape.json'):
        self.url_base = "https://api.proxyscrape.com/v2/account/datacenter_shared"
        self.state = TinyDB(storage_path)
        self._proxy_data = self.state.table(api_key, cache_size=0)
        self.api_key = api_key
        self.cyclic = cyclic

    @property
    def params(self):
        return {
            'type': 'getproxies',
            'country': 'all',
            'protocol': 'http',
            'format': 'normal',
            'auth': self.api_key
        }

    def get_proxy_list(self):
        def valid_ip(ip):
            return bool(re.match(r'^(\d{1,3}\.){3}\d{1,3}:\d{2,4}$', ip))
        res = requests.get(f'{self.url_base}/proxy-list', params=self.params)
        li = res.text.split()
        if all(list(map(valid_ip, li))):
            return li
        raise Exception(res.text)

    def load(self):
        """ update the internal snapshoot of proxies """
        li = self.get_proxy_list()
        data = [{'key': k, 'proxy': v} for k, v in enumerate(li)]
        data += [{'key': -1, 'current': 0}]
        self.state.drop_table(self.api_key)
        self._proxy_data = self.state.table(self.api_key, cache_size=0)
        self._proxy_data.insert_multiple(data)

    @property
    def proxies(self):
        """ returns a snapshot of proxies """
        return [x['proxy'] for x in self._proxy_data.all()[:-1]]

    @property
    def proxy(self):
        """ returns the current selected proxy """
        if not self._proxy_data.all():
            self.load()
        curr = self._proxy_data.search(Query().key == -1)[0]['current']
        return self._proxy_data.search(Query().key == curr)[0]['proxy']

    def next_proxy(self) -> str:
        """ advance to the next proxy in the local snapshot and return the value,
        if cyclic is true all ip was used then returns the first and start again
        else if cyclic is false and all ip was used then start again after request ips"""
        curr = self._proxy_data.search(Query().key == -1)[0]['current']
        if curr < len(self._proxy_data.all()[:-2]):
            self._proxy_data.update(increment('current'), Query().key == -1)
        elif self.cyclic:
            self._proxy_data.update(set('current', 0), Query().key == -1)
        else:
            self.load()
        return self.proxy
