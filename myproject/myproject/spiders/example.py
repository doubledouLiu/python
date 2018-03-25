# -*- coding: utf-8 -*-
import scrapy
from myproject.items import MyItem



class QuotesSpider(scrapy.Spider):
    name = "quotes"

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_page1(self, response):
        item = MyItem()
        item['main_url'] = response.url
        request = scrapy.Request("http://www.example.com/some_page.html",
                             callback=self.parse_page2)
        request.meta['item'] = item
        return request

    def parse_page2(self, response):
        item = response.meta['item']
        item['other_url'] = response.url
        return item
