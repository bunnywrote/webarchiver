from scrapy.crawler import CrawlerProcess
from recursiveCrawling.recursiveCrawling.spiders import Spider

def main():
    domainName = "http://quotes.toscrape.com";
    spider = Spider.StationDetailSpider()
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(spider)
    process.start()

if __name__ == '__main__':
    main()