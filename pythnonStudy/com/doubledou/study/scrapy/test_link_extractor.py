#-*- coding: utf-8 -*-
__author__ = 'liudoudou'
import re
from scrapy.http import HtmlResponse, XmlResponse
import unittest


class base:
    class LinkExtractorTestBase(unittest.TestCase):
        extractor_cls = None
        escape_whitespace = False

        def setUp(self):
            self.response = HtmlResponse(url='http://example.com/index', body='link_extractor')

        def test_urls_type(self):
            lx = self.extractor_cls()
            self.assertTrue(all(isinstance(link.url, str) for link in lx.extract_links(self.response)))


