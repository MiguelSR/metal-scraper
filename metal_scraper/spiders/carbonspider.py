import json
import re
import os
import scrapy

from metal_scraper.items import BandDetails

LOCALHOST = True

class CarbonSpider(scrapy.Spider):
    name = "carbonspider"
