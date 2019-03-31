# Metal Scraper

Forked from @MiguelSR.

This now scrapes the entirety of Metal-Archives.

## Description

This is a simple scraper made with Scrapy to get information about Metal bands (scraping data from metal-archives.com).

Run `scrapy crawl steelspider -o items.json` in main folder and you will get every band listed in metal-archives.com in your items.json file.
Scrapy provides automagically other exporting formats, so you can do `scrapy crawl steelspider -o items.csv` and get the output in csv.

### Parameters:

* Complexity (optional): Run `scrapy crawl steelspider -a complexity=1` (any number above 0, actually) and it will fetch extra fields such as region, formation year, etc.

### Band structure:

* name
* metalarchives_id
* style
* country
* region (complexity >= 1)
* city (complexity >= 1)
* formation_year (complexity >= 1)
* lyrical_themes (complexity >= 1)

## Requirements:

* Python
* Scrapy
