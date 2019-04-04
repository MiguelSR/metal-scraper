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
    logo_url = scrapy.Field()
    photo_url = scrapy.Field()
    band_comment = scrapy.Field()
    stats = scrapy.Field()
    albums = scrapy.Field()
    audit_trail = scrapy.Field()
    related_bands = scrapy.Field()
    albums = scrapy.Field()
    audit_trail = scrapy.Field()
