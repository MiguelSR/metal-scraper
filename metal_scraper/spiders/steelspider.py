# -*- coding: utf-8 -*-
import json
import re
import os
import scrapy
import time
import savepagenow

from metal_scraper.items import Band

# TODO work out a better way for setting env vars...docker maybe???
LOCALHOST = False


class SteelSpider(scrapy.Spider):
    """
    SteelSpider is the scraper designed to pull the list of bands and all relevant information about them into a 
    local .json file. Another scraper will be launched on the band URLs and metal archive ids grabbing all relevant 
    information.
    """
    name = "steelspider"
    if LOCALHOST:
        allowed_domains = ["localhost"]
        start_urls = [
            'http://localhost:8000/metal_scraper/test_data/search.json'
        ]
    else:
        allowed_domains = ["metal-archives.com", "metal-archives.local"]
        start_urls = [
            'https://www.metal-archives.com/search/ajax-advanced/searching/bands?bandName=*'
        ]
    fetched = 0

    def __init__(self, complexity=0):
        self.complexity = int(complexity)

    def parse(self, response):
        response_data = json.loads(response.body)
        total_records = response_data['iTotalRecords']

        for item in response_data['aaData']:
            band = Band()
            match = re.search('<a href=".*/(\d+)">(.*)<\/a>.*', item[0])
            band['name'] = match.group(2)
            band['metalarchives_id'] = match.group(1)

            # Regex to extract the band URL from the <a> tag
            url = re.search('href="([^"]*)', item[0])
            band['url'] = url.group(1)
            band["wayback_link"] = savepagenow.capture_or_cache(band['url'])
            yield band

        if self.fetched < total_records:
            url = self.start_urls[0] + '&iDisplayStart=%s' % self.fetched
            yield scrapy.Request(url, callback=self.parse)
        yield
