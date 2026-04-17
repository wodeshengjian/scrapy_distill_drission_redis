"""Demo Distributed Spider"""
import scrapy
from scrapy_redis.spiders import RedisSpider
from src.spider.items import CrawlItem
import datetime
import time


class DemoSpider(RedisSpider):
    name = 'demo_spider'
    redis_key = 'demo:start_urls'
    allowed_domains = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = kwargs.get('start_urls', ['https://httpbin.org/html'])

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, meta={'use_drission': True})

    def make_request_from_data(self, data):
        url = data.decode('utf-8') if isinstance(data, bytes) else str(data)
        return scrapy.Request(url, callback=self.parse, meta={'use_drission': True})

    def parse(self, response):
        self.logger.info(f'Crawling: {response.url}')
        
        item = CrawlItem()
        item['title'] = response.xpath('//title/text()').get()
        item['url'] = response.url
        item['content'] = response.xpath('//body//text()').getall()
        item['created_at'] = datetime.datetime.now().isoformat()
        item['source'] = 'demo_spider'
        
        yield item
        
        self.logger.info(f'Parsed: {response.url}')
        
        for href in response.xpath('//a/@href').getall()[:5]:
            full_url = response.urljoin(href)
            if full_url.startswith('http'):
                yield scrapy.Request(full_url, callback=self.parse, meta={'use_drission': True})
        
        time.sleep(1)