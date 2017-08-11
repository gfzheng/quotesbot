# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join

class QuotesbotItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    text = Field()
    author = Field()
    tag = Field()
    crawled = Field()
    spider = Field()
    url = Field()

class QuotesbotLoader(ItemLoader):
    default_item_class = QuotesbotItem
    default_input_processor = MapCompose(lambda s: s.strip())
    default_output_processor = TakeFirst()
    description_out = Join()