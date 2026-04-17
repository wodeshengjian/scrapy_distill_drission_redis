"""Proxy Pool Manager"""
import random
import requests
from src.utils.redis_client import get_redis_client


class ProxyPool:
    """Redis-based Proxy Pool"""
    def __init__(self):
        self.redis_client = get_redis_client()
        self.proxy_key = 'proxy:pool'
        self.bad_proxy_key = 'proxy:bad'

    def add_proxy(self, proxy):
        """Add a proxy to pool"""
        self.redis_client.sadd(self.proxy_key, proxy)
        self.redis_client.srem(self.bad_proxy_key, proxy)

    def get_proxy(self):
        """Get a random proxy"""
        proxy = self.redis_client.srandmember(self.proxy_key)
        if proxy:
            return proxy.decode('utf-8') if isinstance(proxy, bytes) else proxy
        return None

    def remove_proxy(self, proxy):
        """Remove a bad proxy"""
        self.redis_client.srem(self.proxy_key, proxy)
        self.redis_client.sadd(self.bad_proxy_key, proxy)

    def get_all_proxies(self):
        """Get all proxies"""
        proxies = self.redis_client.smembers(self.proxy_key)
        return [p.decode('utf-8') if isinstance(p, bytes) else p for p in proxies]

    def get_proxy_count(self):
        """Get proxy count"""
        return self.redis_client.scard(self.proxy_key)

    def validate_proxy(self, proxy, timeout=5):
        """Validate proxy"""
        try:
            response = requests.get(
                'http://httpbin.org/ip', 
                proxies={'http': proxy, 'https': proxy}, 
                timeout=timeout
            )
            return response.status_code == 200
        except Exception:
            return False

    def refresh_proxies(self, proxy_list):
        """Refresh proxy list"""
        for proxy in proxy_list:
            if self.validate_proxy(proxy):
                self.add_proxy(proxy)

    def auto_clean(self):
        """Auto clean invalid proxies"""
        all_proxies = self.get_all_proxies()
        for proxy in all_proxies:
            if not self.validate_proxy(proxy):
                self.remove_proxy(proxy)