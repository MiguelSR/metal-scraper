# -*- coding: utf-8 -*-
import json
import scrapy

import urllib
from bs4 import BeautifulSoup

from metal_scraper.items import Band


class IronSpider(scrapy.Spider):
    name = "ironspider"
    allowed_domains = ["metal-archives.com", "metal-archives.local"]
    start_urls = ()
    fetched = 0

    def __init__(self):
        bands = self.getrecords()

        for band in bands:
            url = band['url']

            page = urllib.request.urlopen(url)

            soup = BeautifulSoup(page, 'html.parser')

            print(soup)



    # gets a list of records to start crawling urls
    # should probably be refactored into a db process
    def getrecords(self):
        filename = 'items.json'
        if filename:
            with open(filename, 'r') as f:
                bands = json.load(f)

        return bands
