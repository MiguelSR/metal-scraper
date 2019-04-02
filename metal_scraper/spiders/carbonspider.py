import json
import re
import os
import scrapy

from metal_scraper.items import BandDetails, Band

LOCALHOST = True

class CarbonSpider(scrapy.Spider):
    """
    CarbonSpider is part of the alloy spiders for 
    scraping metal archives. It runs after SteelSpider returns
    a list bands, individually scraping each page.
    TODO: member parsing for past and current line-ups
    """
    name = "carbonspider"

    def __init__(self, band=None):
        self.start_urls = [ band.url ]

    def parse(self, response):
        band_details = BandDetails(self.band)
        band_details["logo_url"] = response.css("div.band_name_img a::attr(href)").get()

        keys = response.css("div dl dt::text").getall()
        keys = [ key.lower().strip(":").replace(" ", "_") for key in keys ]

        values = response.css("div dl dd::text").getall()
        values = [ value.lower().strip() for value in values ]

        band_details["stats"] = dict(zip(keys, values))

        audit_keys = ["added_on", "modified_on"]
        audit_values = response.css("#auditTrail td::text").getall()
        audit_values = [item.split("on:")[1].strip() for item in audit_values if "on:" in item]
        band_details["audit_trail"] = dict(zip(audit_keys, audit_values))

        yield band_details
