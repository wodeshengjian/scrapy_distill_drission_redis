"""Redis Client with Mock Support"""
import time
import json
from collections import deque
from threading import Lock


class MockRedis:
    """In-memory mock Redis implementation"""
    def __init__(self):
        self.data = {}
        self.lock = Lock()
    
    def set(self, key, value, ex=None):
        with self.lock:
            self.data[key] = {
                'value': value,
                'expire': time.time() + ex if ex else None
            }
    
    def get(self, key):
        with self.lock:
            if key not in self.data:
                return None
            item = self.data[key]
            if item['expire'] and time.time() > item['expire']:
                del self.data[key]
                return None
            return item['value']
    
    def delete(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]
                return 1
            return 0
    
    def exists(self, key):
        return 1 if self.get(key) else 0
    
    def lpush(self, key, *values):
        with self.lock:
            if key not in self.data:
                self.data[key] = {'value': deque(), 'expire': None}
            for value in values:
                self.data[key]['value'].appendleft(value)
            return len(self.data[key]['value'])
    
    def rpush(self, key, *values):
        with self.lock:
            if key not in self.data:
                self.data[key] = {'value': deque(), 'expire': None}
            for value in values:
                self.data[key]['value'].append(value)
            return len(self.data[key]['value'])
    
    def rpop(self, key):
        with self.lock:
            if key not in self.data or not self.data[key]['value']:
                return None
            return self.data[key]['value'].pop()
    
    def lpop(self, key):
        with self.lock:
            if key not in self.data or not self.data[key]['value']:
                return None
            return self.data[key]['value'].popleft()
    
    def llen(self, key):
        with self.lock:
            if key not in self.data:
                return 0
            return len(self.data[key]['value'])
    
    def sadd(self, key, *members):
        with self.lock:
            if key not in self.data:
                self.data[key] = {'value': set(), 'expire': None}
            original_len = len(self.data[key]['value'])
            self.data[key]['value'].update(members)
            return len(self.data[key]['value']) - original_len
    
    def sismember(self, key, member):
        with self.lock:
            if key not in self.data:
                return 0
            return 1 if member in self.data[key]['value'] else 0
    
    def smembers(self, key):
        with self.lock:
            if key not in self.data:
                return set()
            return self.data[key]['value']
    
    def scard(self, key):
        with self.lock:
            if key not in self.data:
                return 0
            return len(self.data[key]['value'])
    
    def srandmember(self, key):
        with self.lock:
            if key not in self.data or not self.data[key]['value']:
                return None
            members = list(self.data[key]['value'])
            return members[0] if members else None
    
    def srem(self, key, *members):
        with self.lock:
            if key not in self.data:
                return 0
            original_len = len(self.data[key]['value'])
            self.data[key]['value'].difference_update(members)
            return original_len - len(self.data[key]['value'])
    
    def hset(self, key, field, value):
        with self.lock:
            if key not in self.data:
                self.data[key] = {'value': {}, 'expire': None}
            self.data[key]['value'][field] = value
    
    def hget(self, key, field):
        with self.lock:
            if key not in self.data:
                return None
            return self.data[key]['value'].get(field)
    
    def hgetall(self, key):
        with self.lock:
            if key not in self.data:
                return {}
            return self.data[key]['value']
    
    def incr(self, key):
        with self.lock:
            if key not in self.data:
                self.data[key] = {'value': 0, 'expire': None}
            self.data[key]['value'] += 1
            return self.data[key]['value']
    
    def decr(self, key):
        with self.lock:
            if key not in self.data:
                self.data[key] = {'value': 0, 'expire': None}
            self.data[key]['value'] -= 1
            return self.data[key]['value']
    
    def flushdb(self):
        with self.lock:
            self.data.clear()


mock_redis = MockRedis()


def get_redis_client():
    """Get Redis client (real or mock)"""
    try:
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.ping()
        return r
    except Exception:
        return mock_redis