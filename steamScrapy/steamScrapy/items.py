# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SteamscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    current_price = scrapy.Field()
    original_price = scrapy.Field()
    discount = scrapy.Field()
    releaseday = scrapy.Field()
    score = scrapy.Field()
    review = scrapy.Field()
    link = scrapy.Field()

