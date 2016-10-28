import os
import urllib

import lxml
import scrapy
from scrapy.crawler import CrawlerProcess

class PageSpider(scrapy.Spider):
    name = "quotes"

    def __init__(self, *args, **kwargs):
        super(PageSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        urls = self.get_pages()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page

        urllib.urlretrieve(self.domain + '/page/1', "page1.html")

        with open(filename, 'wb') as f:
            root = lxml.html.fromstring(response.body)

            lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head")

            print(lxml.html.tostring(root, method="text"))
          #  f.write(page)
        self.log('Saved file %s' % filename)

    def get_pages(self):
        count = 1
        result = []
        for i in range(count):
            result.append(self.domain + '/page/' + str(i))
        return result

def main():
    domainName = "http://quotes.toscrape.com";
    spider = PageSpider()
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })

    process.crawl(spider, domain = domainName)
    process.start()

if __name__ == '__main__':
    main()