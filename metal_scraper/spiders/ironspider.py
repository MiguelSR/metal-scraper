# -*- coding: utf-8 -*-
import json
import logging
import re

import urllib
from bs4 import BeautifulSoup

from metal_scraper.items import Band

log = logging.getLogger('ironspider')
log.setLevel(logging.DEBUG)

#TODO: BAND MEMBERS, PAST AND CURRENT

LOCALHOST = True

def run(path):
    bands = get_bandlist(path)

    for band in bands:
        url = band['url']

        page = urllib.request.urlopen(url)

        soup = BeautifulSoup(page, 'html.parser')
        # Get the band logo
        logo_div = soup.find("a", {"id": "logo"})
        band['logo'] = logo_div['href']
        band.update(get_band_stats(soup))
        band["albums"] = get_complete_discography(band["metalarchives_id"])
        band["related_artists"] = get_related_artist_ma_ids(band["metalarchives_id"])
        #print(f'band: {band}')

# gets a list of records to start crawling urls
# should probably be refactored into a db process
def get_bandlist(path):
    """
    returns list of bands urls to be crawled
    """
    if path:
        with open(path, 'r') as f:
            bands = json.load(f)
        return bands
    # raise error

def get_band_stats(soup):
    """
    Returns all statistical information about a band.
    """
    dts = soup.find_all("dt")
    stats_keys = []
    for key in dts:
        stats_keys.append(key.get_text().lower().replace(" ", "_").strip(":"))
    dds = soup.find_all("dd")
    stats_values = []
    for value in dds:
        stats_values.append(value.get_text().lower().replace("\n", " ").replace("\t", " ").strip())
    band_stats = dict(zip(stats_keys, stats_values))
    return band_stats

def get_complete_discography(band_id):
    """
    returns the discography for a band
    fun fact: we actually just: 'https://www.metal-archives.com/band/discography/id/3540438154/tab/all' is a link to the full disco
    construction: ma/band/discography/id/<ma_id>/tab/all
    """
    # construct URL
    url = f"https://wwww.metal-archives.com/band/discography/id/{band_id}/tab/all"
    if LOCALHOST:
        url = "http://localhost:8000/metal_scraper/test_data/disco.html"
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')

    rows = soup.find_all("tr")
    albums = []
    
    for row in rows:
        cols = row.findAll('td')
        album = {}
        for idx, col in enumerate(cols):
            # python is really stupid for not having a switch...
            # set up name and url 
            if idx == 0:
                album["name"] = col.find("a").get_text()
                album["url"] = col.find("a")["href"]
                album["album_id"] = album["url"].split("/")[-1]
            elif idx == 1:
                album["type"] = col.get_text().strip()
            elif idx == 2:
                album["year"] = col.get_text().strip()
            elif idx == 3:
                if(col.find("a")):
                    review = {}
                    review["percent_and_count"] = col.find("a").get_text()
                    review["url"] = col.find("a")["href"]
                    album["review"] = review
            else: # set to null
                album = None
        if album:
            albums.append(album)
    return(albums)

def get_related_artist_ma_ids(band_id):
    """
    returns related artists
    https://www.metal-archives.com/band/ajax-recommendations/id/{ma_id}
    """
    url = "https://www.metal-archives.com/band/ajax-recommendations/id/{band_id}"
    if LOCALHOST:
        url = "http://localhost:8000/metal_scraper/test_data/related.html"
    
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find("tbody").findAll("a")
    related_ids = []
    for link in links:
        related_ids.append(link["href"].split("/")[-1])
    return related_ids


