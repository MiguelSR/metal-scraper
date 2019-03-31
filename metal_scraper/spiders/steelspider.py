# -*- coding: utf-8 -*-
import json
import re
import os
import scrapy

from metal_scraper.items import Band

# TODO work out a better way for setting env vars...docker maybe???
LOCALHOST = True

class SteelSpider(scrapy.Spider):
    """
    SteelSpider is the scraper designed to pull the list of bands and all relevant information about them into a 
    local .json file. Another scraper will be launched on the band URLs and metal archive ids grabbing all relevant 
    information.
    """
    name = "steelspider"
    if LOCALHOST:
        allowed_domains = ["../test_data/search.json"]
        start_urls = 'http://www.metal-archives.com/search/ajax-advanced/searching/bands/?'
    else:
        allowed_domains = ["metal-archives.com", "metal-archives.local"]
        start_urls = (
            'http://www.metal-archives.com/search/ajax-advanced/searching/bands/?'
        )
    fetched = 0

    def __init__(self, complexity=0):
        self.complexity = int(complexity)
        if self.complexity > 0:
            self.start_urls = (self.start_urls[0] + "yearCreationFrom=0&yearCreationTo=9999&themes=*&location=*",)

    def parse(self, response):
        response_data = json.loads(response.body)
        total_records = response_data['iTotalRecords']

        for item in response_data['aaData']:
            band = Band()
            match = re.search('<a href=".*/(\d+)">(.*)<\/a>.*', item[0])
            band['name'] = match.group(2)
            band['metalarchives_id'] = match.group(1)

            band['style'] = item[1].strip()

            band['country'] = item[2].strip()

            # Regex to extract the band URL from the <a> tag
            url = re.search('href="([^"]*)', item[0])
            band['url'] = url.group(1)

            if self.complexity > 0:
                geo_info = item[3].split(',')
                band['city'] = geo_info[0].strip()
                if len(geo_info) > 1:
                    band['region'] = geo_info[1].strip()

                band['lyrical_themes'] = item[4].strip()
                band['formation_year'] =  "01/01/" + item[5].strip()

            self.fetched += 1
            yield band

        if self.fetched < total_records:
            url = self.start_urls[0] + '&iDisplayStart=%s' % self.fetched
            yield scrapy.Request(url, callback=self.parse)
        yield
