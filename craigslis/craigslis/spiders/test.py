import hashlib
import os
import scrapy
import htmlmin
from scrapy import Request

from ..items import CraigslisItem


class TestSpyder(scrapy.Spider):
    name = "testSpider"
    allowed_domains = ["https://www.zalando.ch/"]
    start_urls = ["https://www.zalando.ch/herren-accessoires"]

    def start_requests(self):
        urls = self.start_urls
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        file_name = self.hash_url(response.url) + '.html'
        directory = 'testdir'

        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(directory + '/' + file_name, 'wb') as f:
            content = htmlmin.minify(response.body.decode('utf-8'))
            f.write(bytes(content, 'utf-8'))

        for a in response.xpath('//a'):
            item = CraigslisItem()
            item['title'] = a.xpath('text()').extract()
            item['link'] = a.xpath('@href').extract()
            # yield Request(item, callback=self.get_childs)
            self.get_childs(item)


    def hash_url(self, url):
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def get_childs(self, item):
        print(item)