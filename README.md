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
* url

## Requirements:

* Python
* Scrapy
* Pipenv

## Quick Start

1. run `pipenv install`, this will install all the necessary packages. 
2. run `pipenv run scrapy crawl scrapy crawl <spider> -o items.json` 

### Local Testing and Development
1. run `python -m http.server 8000` to start a simple dev server
2. run the commands as you would for production, setting LOCALHOST to true.

## TODOs:
- [ ] figure out a way to do this with env vars
- [ ] host this somewhere where I can have the output of the scrapers dumped into a bucket
- [ ] LICENSE
- [ ] CLI for quickstart, use @itdaniher's thing
- [ ] include complete line up -- stretch goal

