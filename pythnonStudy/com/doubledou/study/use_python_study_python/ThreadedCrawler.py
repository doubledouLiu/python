import time
import threading
import urlparse
from Downloader import *
from MongoCache import *
from ScrapeCallback import *
from AlexaCallback import *
SLEEP_TIME = 5


def ThreadCrawler(seed_url, link_regex, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None, num_retries=1, max_threads=10, timeout=60):
    crawl_queue = [seed_url]
    seen = set([seed_url])
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_tries=1, catch=cache)

    def process_queue():
        while crawl_queue:
            try:
                url = crawl_queue.pop()
            except IndexError:
                break
            else:
                time.sleep(5)
                html = D(url)
                # if html is None:
                #     break
                if scrape_callback:
                    try:
                        links = scrape_callback(url, html) or []
                    except Exception as e:
                        raise e
                        #print 'Error in callback for: {}: {}'.format(url, e)
                    else:
                        for link in links:
                            if re.match(link_regex, link):
                                link = normalize(seed_url, link)
                                if link not in seen:
                                    seen.add(link)
                                    crawl_queue.append(link)

    threads = []
    while threads or crawl_queue:
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and crawl_queue:
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)
        print threads.__len__()
        print crawl_queue.__len__()
    #process_queue()


def normalize(seed_url, link):
    link, _ = urlparse.urldefrag(link)
    return urlparse.urljoin(seed_url, link)


def get_links(html):
    webPage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webPage_regex.findall(html)


if __name__ == '__main__':
    ThreadCrawler('http://example.webscraping.com/', '/(index|view)', cache=MongoCache(), scrape_callback=AlexaCallback())
    print 'finished'