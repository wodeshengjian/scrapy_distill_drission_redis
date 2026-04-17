"""Scrapy Settings"""
import os

BOT_NAME = 'ScraDispage'
SPIDER_MODULES = ['src.spider.spiders']
NEWSPIDER_MODULE = 'src.spider.spiders'

# Redis Configuration
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))

# Distributed Settings
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
SCHEDULER_PERSIST = True

# Crawl Settings
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_IP = 4
DOWNLOAD_DELAY = 2
DOWNLOAD_DELAY_MIN = 1
DOWNLOAD_DELAY_MAX = 5

# Retry Settings
RETRY_ENABLED = True
RETRY_TIMES = 3
RETRY_HTTP_CODES = [403, 429, 500, 502, 503, 504]

# Proxy Settings
PROXY_KEY = 'proxy:pool'
PROXY_ROTATE_INTERVAL = 10
PROXY_VALIDATE_URL = 'http://httpbin.org/ip'

# DrissionPage Settings
DRISSION_PAGE_HEADLESS = True

# Anti-Detect Settings
ANTI_DETECT_RETRY_COUNT = 3

# Fingerprint Settings
FINGERPRINT_ENABLED = True
CANVAS_FINGERPRINT = True
WEBGL_FINGERPRINT = True

# Referer Settings
REFERER_ENABLED = True
REFERER_RANDOMIZE = True

# Downloader Middlewares
DOWNLOADER_MIDDLEWARES = {
    'src.spider.middlewares.UserAgentMiddleware': 100,
    'src.spider.middlewares.HeadersMiddleware': 110,
    'src.spider.middlewares.CookieMiddleware': 120,
    'src.spider.middlewares.ProxyMiddleware': 130,
    'src.spider.middlewares.FingerprintMiddleware': 200,
    'src.spider.middlewares.AntiDetectMiddleware': 210,
    'src.spider.middlewares.RetryMiddleware': 220,
    'src.spider.middlewares.DrissionPageMiddleware': 300,
}

# Item Pipelines
ITEM_PIPELINES = {
    'src.spider.pipelines.RedisPipeline': 300,
    'src.spider.pipelines.FilePipeline': 400,
}

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', 'spider.log')

# User Agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'