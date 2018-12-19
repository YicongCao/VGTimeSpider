# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class VgtimespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GameItem(scrapy.Item):
    name = scrapy.Field()
    nickname = scrapy.Field()
    score = scrapy.Field()
    platform = scrapy.Field()
    date = scrapy.Field()
    dna = scrapy.Field()
    company = scrapy.Field()
    tag = scrapy.Field()
    url = scrapy.Field()
