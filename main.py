from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapy.signalmanager import dispatcher
from metal_scraper.spiders.steelspider import SteelSpider
from metal_scraper.spiders.ironspider import run
import logging

log = logging.getLogger('runner')
log.setLevel(logging.DEBUG)


def spider_results(spider):
    results = []

    def crawler_results(signal, sender, item, response, spider):
        log.debug(f'len(results): {len(results)}')
        if len(results) == 50:  #1 page of results 10 for testing
            log.debug("dumping results")
            run(results)
            results.clear()
        results.append(item)

    dispatcher.connect(crawler_results, signal=signals.item_passed)

    process = CrawlerProcess(get_project_settings())
    process.crawl(spider)
    process.start(
    )  # the script will block here until the crawling is finished
    return results


if __name__ == '__main__':
    res = spider_results(SteelSpider)
    run(res)
