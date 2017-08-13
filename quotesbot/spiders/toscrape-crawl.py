# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisCrawlSpider
#from scrapy_redis.spiders import RedisSpider


class ToScrapeSpiderCrawl(RedisCrawlSpider):
    """Spider that reads urls from redis queue (toscrawl:start_urls)."""
    name = 'toscrape-crawl'
    redis_key = 'toscrawl:start_urls'

    rules = (
        # follow all links
        Rule(LinkExtractor(), callback='parse_page', follow=True),
    )

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(ToScrapeSpiderCrawl, self).__init__(*args, **kwargs)

    def parse_page(self, response):
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

