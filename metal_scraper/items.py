# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Band(scrapy.Item):
    name = scrapy.Field()
    metalarchives_id = scrapy.Field()
    style = scrapy.Field()
    country = scrapy.Field()
    region = scrapy.Field()
    city = scrapy.Field()
    status = scrapy.Field()
    formation_year = scrapy.Field()
    breakup_year = scrapy.Field()
    lyrical_themes = scrapy.Field()
    url = scrapy.Field()
