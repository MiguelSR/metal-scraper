# -*- coding: utf-8 -*-
import json
import logging

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

        print(f'band: {band}')




# gets a list of records to start crawling urls
# should probably be refactored into a db process
def get_records(path):
    if path:
        with open(path, 'r') as f:
            bands = json.load(f)
        return bands
    # raise error
