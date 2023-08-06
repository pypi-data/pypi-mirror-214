"""Main module."""

import time
from urllib3 import ProxyManager, make_headers
import urllib3


class Proxy:
    def __init__(self, http_proxy, change_port, sock5_port=0) -> None:
        # accept in format of 1.1.1.1:1565:abc:xyz
        self.ip = http_proxy.split(":")[0]
        self.http_port = http_proxy.split(":")[1]
        self.username = http_proxy.split(":")[2]
        self.password = http_proxy.split(":")[3]
        self.proxy_ip = self.get_ip()
        self.sock5_port = sock5_port

        self.change_port = change_port

    def get_change_url(self):
        return f"http://{self.ip}:{self.change_port}/change_ip?t={self.username}{self.password}"

    def change_ip(self, delay=25):
        http = urllib3.PoolManager()
        x = http.request('GET', self.get_change_url())
        if "success" not in x.data.decode('utf-8').lower():
            raise ValueError("Invalid Credentials")
        time.sleep(delay)
        return self.get_ip() 

    def get_http_proxy(self):
        return f'http://{self.username}:{self.password}@{self.ip}:{self.http_port}'
    
    def get_sock5_proxy(self):
        return f'socks5://{self.username}:{self.password}@{self.ip}:{self.sock5_port}'
    
    def __str__(self) -> str:
        return self.get_http_proxy()
    
    def get_ip(self):
        proxy = urllib3.ProxyManager(f"http://{self.ip}:{self.http_port}", proxy_headers=make_headers(proxy_basic_auth=f'{self.username}:{self.password}'))
        r = proxy.request('GET', 'https://api.ipify.org/')
        proxy_ip = r.data.decode('utf-8')
        self.proxy_ip = proxy_ip
        return self.proxy_ip
        
if __name__ == "__main__":
    p = Proxy(input(), input())
    print(p.proxy_ip)
    print(p.change_ip(30))
    print(p.proxy_ip)