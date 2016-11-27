import hashlib
import os

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import htmlmin
from ..items import LinkItem

class TestSpider(CrawlSpider):
    name = 'test'
    directory = 'testdir'
    allowed_domains = ["www.zalando.ch"]

    def __init__(self, *args, **kwargs):
        super(TestSpider, self).__init__(*args, **kwargs)

        if len(kwargs) > 0:
            self.start_urls = [kwargs['start_urls']]

    rules = (
        #Rule((LinkExtractor(allow=(),restrict_xpaths="//a")),callback='parse_item', follow=True),
        #Rule(LinkExtractor(allow=''), callback='parse_item')
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a',)), callback="parse_items", follow=True),
    )

    def parse_items(self, response):
        # print(response.xpath("//div").extract()[0])
        # file_name = self.hash_url(response.url) + '.html'
        file_name = response.url + '.html'

        # item = LinkItem()
        # item["title"] = response.url
        # item["link"] = response.url
        # return item;

        if not os.path.exists(self.directory):
            os.makedirs(self.directory)

        with open(self.directory + '/' + file_name.replace("/","_")[23:], 'wb') as f:
            content = htmlmin.minify(response.body.decode('utf-8'))
            f.write(bytes(content, 'utf-8'))

    def hash_url(self, url):
        return hashlib.md5(url.encode('utf-8')).hexdigest()