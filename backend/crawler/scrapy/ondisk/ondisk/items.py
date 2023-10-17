# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OndiskItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    cat1 = scrapy.Field()
    cat2 = scrapy.Field()
    idx = scrapy.Field()
    txt = scrapy.Field()
    Lvl19 = scrapy.Field()
