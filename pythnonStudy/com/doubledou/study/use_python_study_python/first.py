import urllib2
import re
import itertools
import urlparse
import robotparser
import datetime
import time
from bs4 import BeautifulSoup
import lxml.html
import csv
import random

# def download(url) :
#         print 'downloading:', url
#         try :
#             html = urllib2.urlopen(url).read()
#         except urllib2.URLError as e:
#             print 'Download error:',e.reason
#             html = None
#         return html

# def download(url, number_tries = 2):
#         print 'downloading:', url
#         try :
#             html = urllib2.urlopen(url).read()
#         except urllib2.URLError as e:
#             print 'Download error:',e.reason
#             html = None
#             if(number_tries > 0):
#                if hasattr(e,'code') and 500 <= e.code <=600:
#                    return download(url, number_tries -1)
#         return html


def download(url, user_agent='wswp', proxy=None, num_tries=2):
    print 'downloading:', url
    headers = {'User-agent': user_agent}
    request = urllib2.Request(url, headers=headers)

    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))

    html = None
    try:
        html = opener.open(request).read()
    except urllib2.URLError as e:
        print 'Url error:', e.reason
        html = None
        if num_tries > 0:
            if hasattr(e, 'code') and 500 <= e.code <= 600:
                return download(url, num_tries-1)
    except Exception as e:
        print 'error:', e
    return html


def crawl_sitemap(url):
    sitemap = download(url)
    links = re.findall('<loc>(.*?)</loc>', sitemap)
    for link in links:
        download(link)


def crawl_by_id():
    max_errors = 5
    num_errors = 0
    for page in itertools.count(1):
        url = 'http://example.webscraping.com/view/-%d' % page
        html = download(url)
        if html is None:
            num_errors += 1
            if num_errors == max_errors:
                break
        else:
            num_errors = 0


def get_links(html):
    webPage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webPage_regex.findall(html)


class Throttle:
    # add a delay between download to the same domain
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_sec = self.delay - (datetime.datetime.now() - last_accessed).seconds
            if sleep_sec > 0:
                time.sleep(sleep_sec)
        self.domains[domain] = datetime.datetime.now()


def group_crawler():
    url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
    html = download(url)
    soup = BeautifulSoup(html)
    tr = soup.find(attrs={'id': 'places_area__row'})
    td = tr.find(attrs={'class': 'w2p_fw'})
    area = td.text
    print area


def lxml_crawler():
    url = 'http://example.webscraping.com/places/view/United-Kingdom-239'
    html = download(url)
    tree = lxml.html.fromstring(html)
    td = tree.cssselect('tr#places_area__row>td.w2p_fw')[0]
    area = td.text_content()
    print area

if __name__ == '__main__':
    crawl_sitemap('http://example.webscraping.com/sitemap.xml')
    # crawl_by_id()
    #lxml_crawler()
    print 'finished'