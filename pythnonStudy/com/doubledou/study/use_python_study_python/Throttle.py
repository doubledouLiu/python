import urlparse
import time
import datetime


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
