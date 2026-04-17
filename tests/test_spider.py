"""Spider Tests"""
import unittest
from src.utils.redis_client import get_redis_client
from src.spider.proxy_pool.manager import ProxyPool


class TestRedisClient(unittest.TestCase):
    """Test Redis client"""
    def setUp(self):
        self.client = get_redis_client()
    
    def test_set_get(self):
        """Test set and get"""
        self.client.set('test_key', 'test_value')
        self.assertEqual(self.client.get('test_key'), 'test_value')
    
    def test_sadd_smembers(self):
        """Test set operations"""
        self.client.sadd('test_set', 'a', 'b', 'c')
        members = self.client.smembers('test_set')
        self.assertIn('a', members)


class TestProxyPool(unittest.TestCase):
    """Test proxy pool"""
    def setUp(self):
        self.pool = ProxyPool()
    
    def test_add_get_proxy(self):
        """Test add and get proxy"""
        self.pool.add_proxy('http://127.0.0.1:8888')
        proxy = self.pool.get_proxy()
        self.assertIsNotNone(proxy)


if __name__ == '__main__':
    unittest.main()