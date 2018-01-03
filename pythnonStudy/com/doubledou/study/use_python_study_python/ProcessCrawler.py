import time
import re
import urlparse
import threading
import multiprocessing
from MongoCache import *
from MongoQueue import *
from Downloader import *
from AlexaCallback import *
SLEEP_TIME = 5


def ThreadCrawler(seed_url, link_regex, delay=5, cache=None, scrape_callback=None, user_agent='wswp', proxies=None,
                  max_thread=10, timeout=300):
    crawl_queue = MongoQueue(client=MongoClient('localhost', 27017), timeout=timeout)
    crawl_queue.clear()
    crawl_queue.push(seed_url)
    seen = set([seed_url])
    D = Downloader(delay=delay, user_agent=user_agent, proxies=proxies, num_tries=1, catch=cache)

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
            except IndexError:
                break
            else:
                time.sleep(5)
                html = D(url)
                if html is None:
                    continue
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
                                    crawl_queue.push(link)
                crawl_queue.complete(url)

    threads = []
    while threads or crawl_queue.peek():
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_thread and crawl_queue.peek():
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)
        time.sleep(SLEEP_TIME)
        print 'thread', threads.__len__()
    #process_queue()


def normalize(seed_url, link):
    link, _ = urlparse.urldefrag(link)
    return urlparse.urljoin(seed_url, link)


def process_crawler():
    num_cpu = multiprocessing.cpu_count()
    print 'Starting {} processes'.format(num_cpu)
    processes = []
    for i in range(num_cpu):
        p = multiprocessing.Process(target=ThreadCrawler(seed_url='http://example.webscraping.com/', link_regex='/(index|view)', scrape_callback=AlexaCallback(), cache=MongoCache()), name=i + 'process')
        p.start()
        processes.append(p)
    for p in processes:
        p.join()
    print 'process', processes.__len__()


if __name__ == '__main__':
    #process_crawler()
    ThreadCrawler('http://example.webscraping.com/', '/(index|view)', cache=MongoCache(), scrape_callback=AlexaCallback())
    print 'finished'
