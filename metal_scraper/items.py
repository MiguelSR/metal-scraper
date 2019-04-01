# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Band(scrapy.Item):
    name = scrapy.Field()
    metalarchives_id = scrapy.Field()
    url = scrapy.Field()

class BandDetails(Band):
    logo_url = scrapy.Field()
    stats = scrapy.Field()

