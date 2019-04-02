import json
import re
import os
import scrapy

from metal_scraper.items import Band

class CarbonSpider(scrapy.Spider):
    """
    CarbonSpider is part of the alloy spiders for 
    scraping metal archives. It runs after SteelSpider returns
    a list bands, individually scraping each page.
    TODO: member parsing for past and current line-ups
    TODO: set up pipelines to download logo
    TODO: store all this shit in an s3 bucket
    """
    name = "carbonspider"

    def __init__(self, url):
        self.start_urls = [ url ]

    def parse(self, response):
        band = Band()
        band["name"]
        band["logo_url"] = response.css("div.band_name_img a::attr(href)").get()

        keys = response.css("div dl dt::text").getall()
        keys = [ key.lower().strip(":").replace(" ", "_") for key in keys ]

        values = response.css("div dl dd::text").getall()
        values = [ value.lower().strip() for value in values ]

        band["stats"] = dict(zip(keys, values))

        audit_keys = ["added_on", "modified_on"]
        audit_values = response.css("#auditTrail td::text").getall()
        audit_values = [item.split("on:")[1].strip() for item in audit_values if "on:" in item]
        band["audit_trail"] = dict(zip(audit_keys, audit_values))

        yield band
