# -*- coding: utf-8 -*-
import json
import re

import scrapy

from metal_scraper.items import Band


class SteelSpider(scrapy.Spider):
    name = "steelspider"
    allowed_domains = ["metal-archives.com"]
    start_urls = (
        'http://www.metal-archives.com/search/ajax-advanced/searching/bands/?',
    )
    fetched = 0

    def parse(self, response):
        response_data = json.loads(response.body)
        total_records = response_data['iTotalRecords']

        for item in response_data['aaData']:
            band = Band()

            match = re.search('<a href="(.*?)">(.*)<\/a>.*', item[0])
            band['name'] = match.group(2)
            band['link'] = match.group(1)
            band['style'] = item[1]
            band['country'] = item [2]
            self.fetched += 1
            yield band

        if self.fetched < total_records:
            url = self.start_urls[0] + 'iDisplayStart=%s' % self.fetched
            yield scrapy.Request(url, callback=self.parse)
        yield
