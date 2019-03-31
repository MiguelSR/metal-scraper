# -*- coding: utf-8 -*-
import json
import logging
import re

import urllib
from bs4 import BeautifulSoup

from metal_scraper.items import Band

log = logging.getLogger('ironspider')
log.setLevel(logging.DEBUG)


def run(path):
    bands = get_records(path)

    for band in bands:
        url = band['url']

        page = urllib.request.urlopen(url)

        soup = BeautifulSoup(page, 'html.parser')

        # Get the band logo
        logo_div = soup.find("a", {"id": "logo"})
        band['logo'] = logo_div['href']

        # Band stats:
        dts = soup.find_all("dt")
        stats_keys = []
        for key in dts:
            stats_keys.append(key.get_text().lower().replace(" ", "_"))
        print(f"stats_keys: {stats_keys}")
        dds = soup.find_all("dd")
        stats_values = []
        for value in dds:
            stats_values.append(value.get_text().lower())
        band_stats = dict(zip(stats_keys, stats_values))
        # m-a sucks, let's do some formatting here before adding the stat block to the stupid fucking 
        # shitty dictionary
        band.update(band_stats)

        print(f'band: {band}')




# gets a list of records to start crawling urls
# should probably be refactored into a db process
def get_records(path):
    if path:
        with open(path, 'r') as f:
            bands = json.load(f)
        return bands
    # raise error
