##-*- coding: utf-8 -*-
__author__ = 'liudoudou'
from test_item import MyItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import XMLFeedSpider
from scrapy.spiders import CSVFeedSpider
from scrapy.spiders import SitemapSpider
import scrapy


class TestItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()


class MySpider1(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/1.html', 'http://www.example.com/2.html', 'http://www.example.com/3.html', ]

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)


class MySpider2(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']

    start_urls = [
        'http://www.example.com/1.html',
        'http://www.example.com/2.html',
        'http://www.example.com/3.html',
    ]

    def parse(self, response):
        sel = scrapy.Selector(response)
        for h3 in response.xpath('//h3').extract():
            yield {'title': h3}
        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)


class MySpider3(scrapy.Spider):
    name = 'example.com'
    allowed_domains = ['example.com']

    def start_request(self):
        yield scrapy.Request('http://www.example.com/1.html', self.parse)
        yield scrapy.Request('http://www.example.com/2.html', self.parse)
        yield scrapy.Request('http://www.example.com/3.html', self.parse)

    def parse(self, response):
        for h3 in response.xpath('//h3').extract():
            yield MyItem(title=h3)

        for url in response.xpath('//a/href').extract():
            yield scrapy.Request(url, callback=self.parse)


class MySpider4(CrawlSpider):
    name = 'example.com'
    allowed_domains = ['example.com']

    rules = (
        Rule(LinkExtractor(allow=('category\.php', ), deny=('subsection\.php',))),
        Rule(LinkExtractor(allow=('item\.php', )), callback='parse_item'),
    )

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)

        item = TestItem()
        item['id'] = response.xpath('//td[@id="item_id"]/text()').re(r'ID: (\d+)')
        item['name'] = response.xpath('//td[@id="item_name"]/text()').extract()
        item['description'] = response.xpath('//td[@id="item_description"]/text()').extract()

        return item


class MySpider5(XMLFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']

    iterator = 'iternodes'
    itertag = 'item'

    def parse_node(self, response, node):
        self.logger.info('Hi, this is a <%s> node!: %s', self.itertag, ''.join(node.extract()))

        item = TestItem()
        item['id'] = node.xpath('@id').extract()
        item['name'] = node.xpath('name').extract()
        item['description'] = node.xpath('description').extract()
        return item


class MySider6(CSVFeedSpider):
    name = 'example.com'
    allowed_domains = ['example.com']
    start_urls = ['http://www.example.com/feed.csv']

    delimiter = ';'
    quotechar = "'"
    headers = ['id', 'name', 'description']

    def parse_row(self, response, row):
        self.logger.info('Hi, this is a row!: %r', row)

        item = TestItem()
        item['id'] = row['id']
        item['name'] = row['name']
        item['description'] = row['description']

        return item


class MySpider7(SitemapSpider):
    sitemap_urls = ['http://www.example.com/sitemap.xml']
    sitemap_rules = [
        ('/product/', 'parse_product'),
        ('/category/', 'parse_category'),
    ]

    def parse_product(self, response):
        pass

    def parse_category(self, response):
        pass


class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/robots.txt']
    sitemap_rules = [
        ('/shop/', 'parse_shop'),
    ]
    sitemap_follow = ['/sitemap_shops']

    def parse_shop(self, response):
        pass


class MySpider(SitemapSpider):
    sitemap_urls = ['http://www.example.com/robots.txt']
    sitemap_rules = [
        ('/shop/', 'parse_shop'),
    ]

    other_urls = ['http://www.example.com/about']

    def start_requests(self):
        requests = list(super(MySpider, self).start_requests())
        requests += [scrapy.Request(x, self.parse_other) for x in self.other_urls]
        return requests

    def parse_shop(self, response):
        pass

    def parse_other(self, response):
        pass