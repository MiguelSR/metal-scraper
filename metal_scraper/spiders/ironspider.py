# -*- coding: utf-8 -*-
import json
import logging
import re
import time
from scrapy.utils.serialize import ScrapyJSONEncoder
import urllib
from bs4 import BeautifulSoup
import datetime
import savepagenow

log = logging.getLogger('ironspider')
log.setLevel(logging.DEBUG)

import ssl

# This restores the same behavior as before.
context = ssl._create_unverified_context()

#TODO: BAND MEMBERS, PAST AND CURRENT


def run(bands):
    log.debug(f"bands to parse: {len(bands)}")
    band_list = []
    for band in bands:
        log.debug(f"band: {band}")
        url = band['url']

        page = urllib.request.urlopen(url, context=context)

        soup = BeautifulSoup(page, 'html.parser')
        # Get the band logo
        logo_div = soup.find("a", {"id": "logo"})
        band['logo_url'] = logo_div['href'] if logo_div else None
        photo_div = soup.find("a", {"id": "photo"})
        band["photo_url"] = photo_div["href"] if photo_div else None
        comment_div = soup.find("div", {"class": "band_comment"})
        band["band_comment"] = comment_div.get_text() if comment_div else None
        band["stats"] = get_band_stats(soup)
        band["audit_trail"] = get_audit_trail(soup)
        time.sleep(1)
        band["albums"] = get_complete_discography(band["metalarchives_id"])
        band["related_bands"] = get_related_artist_ma_ids(
            band["metalarchives_id"])
        band_list.append(band)
    save_band_list(band_list)


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
        stats_values.append(value.get_text().lower().replace(
            "\n", " ").replace("\t", " ").strip())
    band_stats = dict(zip(stats_keys, stats_values))
    return band_stats


def get_complete_discography(band_id):
    """
    returns the discography for a band
    fun fact: we actually just: 'https://www.metal-archives.com/band/discography/id/3540438154/tab/all' is a link to the full disco
    construction: ma/band/discography/id/<ma_id>/tab/all
    """
    # construct URL
    url = f"https://www.metal-archives.com/band/discography/id/{band_id}/tab/all"
    page = urllib.request.urlopen(url, context=context)
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
                if (col.find("a")):
                    review = {}
                    review["percent_and_count"] = col.find("a").get_text()
                    review["url"] = col.find("a")["href"]
                    album["review"] = review
            else:  # set to null
                album = None
        if album:
            albums.append(album)
    return (albums)


def get_related_artist_ma_ids(band_id):
    """
    returns related artists
    https://www.metal-archives.com/band/ajax-recommendations/id/{ma_id}
    """
    url = f"https://www.metal-archives.com/band/ajax-recommendations/id/{band_id}?showMoreSimilar=1#Similar_artists"
    page = urllib.request.urlopen(url, context=context)
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find("tbody").findAll("a")
    related_ids = []
    for link in links:
        if not "#" in link["href"]:
            related_ids.append(link["href"].split("/")[-1])
    return related_ids


def save_band_list(band_list):
    with open(
            f"data/{int(datetime.datetime.timestamp(datetime.datetime.now()) * 1000)}_bands.json",
            "w+") as f:  # test path for now, get in s3 stuff
        json.dump(band_list, f, cls=ScrapyJSONEncoder)


def get_audit_trail(soup):
    audit_table_div = soup.find("div", {"id": "auditTrail"})
    usrs = audit_table_div.findAll("a")
    users = []
    for u in usrs:
        user = {}
        user["user"] = u.get_text()
        user["profile"] = u["href"]
        users.append(user)
    dates_row = audit_table_div.findAll("tr")[1::1]
    ds = dates_row[0].findAll("td")
    dates = []
    for date in ds:
        d = date.get_text().split(":")[1].strip()
        dates.append(d)

    audit = {}
    audit["added_by"] = users[0]
    audit["added_on"] = dates[0]
    audit["modified_by"] = users[1]
    audit["modified_on"] = dates[1]
    return audit
