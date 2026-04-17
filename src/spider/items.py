"""Scrapy Items"""
import scrapy


class CrawlItem(scrapy.Item):
    """Base crawl item"""
    title = scrapy.Field()
    url = scrapy.Field()
    content = scrapy.Field()
    created_at = scrapy.Field()
    source = scrapy.Field()