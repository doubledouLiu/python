import random
import urllib2
import socket
import urlparse
from Throttle import *


class Downloader:
    def __init__(self, delay=5, user_agent='wswp', proxies=None, num_tries=1, catch=None):
        self.throttle = Throttle(delay)
        self.user_agent = user_agent
        self.proxies = proxies
        self.num_tries = num_tries
        self.catch = catch

    def __call__(self, url):
        result = None
        if self.catch:
            try:
                result = self.catch[url]
            except KeyError:
                pass
            else:
                if self.num_tries > 0 and 500 <= result['code'] < 600:
                    result = None
        if result is None:
            self.throttle.wait(url)
            proxy = random.choice(self.proxies) if self.proxies else None
            headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
            result = self.download(url, headers, proxy, self.num_tries)
            if self.catch:
                self.catch[url] = result
        return result['html']

    def download(self, url, headers, proxy, num_tries, data=None):
        print 'downloading:', url
        request = urllib2.Request(url, headers=headers)
        opener = urllib2.build_opener()
        if proxy:
            proxy_params = {urlparse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib2.ProxyHandler(proxy_params))

        html = None
        try:
            response = opener.open(request, timeout=30)
            html = response.read()
            code = response.code
        except urllib2.URLError as e:
            print 'Url error:', e
            html = None
            if hasattr(e, 'code'):
                code = e.code
                if num_tries > 0 and 500 <= code < 600:
                    return None
        except Exception as e:
            print 'error:', e
        return {'html': html, 'code': code}
