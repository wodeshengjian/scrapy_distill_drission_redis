"""Downloader Middlewares"""
import random
import time
import hashlib
import json
import uuid
from scrapy import signals
from scrapy.exceptions import IgnoreRequest
from DrissionPage import WebPage
from src.utils.redis_client import get_redis_client

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/120.0.0.0',
]

class UserAgentMiddleware:
    """Random User-Agent Middleware"""
    def process_request(self, request, spider):
        request.headers['User-Agent'] = random.choice(USER_AGENTS)

class HeadersMiddleware:
    """Request Headers Middleware"""
    def process_request(self, request, spider):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Upgrade-Insecure-Requests': '1',
        }
        request.headers.update(headers)
        
        if spider.settings.get('REFERER_RANDOMIZE') and 'Referer' not in request.headers:
            request.headers['Referer'] = f'https://{random.choice(["baidu.com", "google.com", "bing.com"])}/'

class CookieMiddleware:
    """Cookie Management Middleware"""
    def __init__(self):
        self.redis_client = get_redis_client()
        self.cookie_key = 'spider:cookies'
        self.session_id = str(uuid.uuid4())

    def process_request(self, request, spider):
        cookies = self.get_cookies()
        if cookies:
            request.cookies.update(cookies)
        request.cookies['session_id'] = self.session_id
        request.cookies['_ga'] = self.generate_ga_id()

    def get_cookies(self):
        cookies = self.redis_client.hgetall(self.cookie_key)
        return {k.decode('utf-8'): v.decode('utf-8') for k, v in cookies.items()} if isinstance(cookies, dict) else {}

    def generate_ga_id(self):
        timestamp = str(int(time.time()))
        random_num = str(random.randint(1000000000, 9999999999))
        return f'GA1.2.{random_num}.{timestamp}'

class ProxyMiddleware:
    """Proxy Rotation Middleware"""
    def __init__(self, proxy_key, rotate_interval):
        self.redis_client = get_redis_client()
        self.proxy_key = proxy_key
        self.current_proxy = None
        self.rotate_interval = rotate_interval
        self.last_rotate_time = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            proxy_key=crawler.settings.get('PROXY_KEY', 'proxy:pool'),
            rotate_interval=crawler.settings.get('PROXY_ROTATE_INTERVAL', 10)
        )

    def process_request(self, request, spider):
        now = time.time()
        if self.current_proxy is None or (now - self.last_rotate_time) > self.rotate_interval or random.random() < 0.1:
            self.current_proxy = self.get_random_proxy()
            self.last_rotate_time = now
        if self.current_proxy:
            request.meta['proxy'] = self.current_proxy

    def get_random_proxy(self):
        proxy = self.redis_client.srandmember(self.proxy_key)
        return proxy.decode('utf-8') if isinstance(proxy, bytes) else proxy

class FingerprintMiddleware:
    """Device Fingerprint Middleware"""
    def __init__(self):
        self.fingerprint = self.generate_fingerprint()

    def generate_fingerprint(self):
        return hashlib.md5(f"{uuid.uuid4()}{time.time()}".encode()).hexdigest()

    def process_request(self, request, spider):
        request.meta['fingerprint'] = self.fingerprint

class AntiDetectMiddleware:
    """AI Anti-Detection Middleware"""
    def __init__(self):
        self.redis_client = get_redis_client()
        self.model_key = 'anti_detect:model'
        self.retry_count = {}

    def process_response(self, request, response, spider):
        url = request.url
        self.retry_count[url] = self.retry_count.get(url, 0)
        
        if self.detect_anti_crawl(response):
            if self.retry_count[url] < 3:
                self.retry_count[url] += 1
                spider.logger.warning(f'Anti-crawl detected, retrying {self.retry_count[url]}/3: {url}')
                time.sleep(2 ** self.retry_count[url] * random.uniform(1, 3))
                return request.copy()
            else:
                spider.logger.error(f'Anti-crawl blocked after 3 retries: {url}')
                raise IgnoreRequest(f'Anti-crawl detected: {url}')
        
        return response

    def detect_anti_crawl(self, response):
        content = response.text.lower()
        anti_patterns = ['captcha', 'blocked', 'denied', 'robot', 'security', 'please wait']
        return any(pattern in content for pattern in anti_patterns)

class RetryMiddleware:
    """Smart Retry Middleware"""
    def process_response(self, request, response, spider):
        if response.status in [403, 429, 500, 502, 503, 504]:
            retry_times = request.meta.get('retry_times', 0)
            if retry_times < 3:
                request.meta['retry_times'] = retry_times + 1
                delay = 2 ** retry_times * random.uniform(1, 3)
                time.sleep(delay)
                return request.copy()
        return response

class DrissionPageMiddleware:
    """DrissionPage Browser Rendering Middleware"""
    def __init__(self):
        self.page = None
        self.request_count = 0

    def process_request(self, request, spider):
        if request.meta.get('use_drission', False):
            if self.page is None:
                self.page = WebPage()
            self.page.get(request.url)
            html = self.page.html
            self.request_count += 1
            
            if self.request_count % 100 == 0:
                self.page.quit()
                self.page = None
            
            from scrapy.http import HtmlResponse
            return HtmlResponse(url=request.url, body=html.encode('utf-8'), encoding='utf-8')
        return None