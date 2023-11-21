# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class OndiskItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    website = scrapy.Field()
    cat1_code = scrapy.Field()
    cat2_code = scrapy.Field()
    category_title = scrapy.Field()
    sub_category_title = scrapy.Field()
    idx = scrapy.Field()
    txt = scrapy.Field()
    Lvl19 = scrapy.Field()
    point = scrapy.Field()
    seller = scrapy.Field()
    partner = scrapy.Field()
    attach_file_size = scrapy.Field()
    time = scrapy.Field()
