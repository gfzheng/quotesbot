# -*- coding: utf-8 -*-
from scrapy_redis.spiders import RedisSpider


class ToScrapeSpiderRedis(RedisSpider):
    """Spider that reads urls from redis queue (myspider:start_urls)."""
    name = 'toscrape-redis'
    redis_key = 'toscrape:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ToScrapeSpiderRedis, self).__init__(*args, **kwargs)

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            yield {
                'text': quote.xpath('./span[@class="text"]/text()').extract_first(),
                'author': quote.xpath('.//small[@class="author"]/text()').extract_first(),
                'tags': quote.xpath('.//div[@class="tags"]/a[@class="tag"]/text()').extract(),
                'url': response.url
            }

#        next_page_url = response.xpath('//li[@class="next"]/a/@href').extract_first()
#        if next_page_url is not None:
#            yield scrapy.Request(response.urljoin(next_page_url))

