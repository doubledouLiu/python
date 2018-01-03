import re


class AlexaCallback:
    def __init__(self, max_urls=1000):
        self.max_urls = max_urls
        self.seed_url = 'http://s3.amazonaws.com/alexa-static/top-1m.csv.zip'

    def __call__(self, url, html):
        urls = []
        webPage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
        list = webPage_regex.findall(html)
        for item in list:
            urls.append(item)
        return urls