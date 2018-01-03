import re
import urlparse
import robotparser
from ScrapeCallback import *
from Downloader import *


def link_crawler(seed_url, link_regex, max_depth=2, user_agent='wswp', proxies=None, scrape_callback=None, catch=None):
    crawler_queue = [seed_url]
    seen = {seed_url: 0}
    output = open('engname.txt', 'w')
    names = []
    #rp = get_robots(seed_url)
    D = Downloader(delay=5, user_agent=user_agent, proxies=proxies, num_tries=1, catch=catch)
    while crawler_queue:
        url = crawler_queue.pop()
        depth = seen[url]
        html = D(url)
        if html is None:
            continue
        res = r'<td class="name_tr" onClick=".*?">(.*?)</td>'
        m_th = re.findall(res, html)
        for name in m_th:
            names.append(name)
        if depth != max_depth:
            for link in get_links(html):
                if re.match(link_regex, link):
                    link = urlparse.urljoin(seed_url, link)
                    if link not in seen:
                        seen[link] = 1
                        crawler_queue.append(link)
                        # links = []
                        # html1 = D(link)
                        # if scrape_callback:
                        #     links.append(scrape_callback(link, html1) or [])
    list = set(names)
    for name in list:
        output.write(name + "\n")
    output.flush()
    output.close()

def get_links(html):
    webPage_regex = re.compile('<a[^>]+href=["\'](.*?)["\']', re.IGNORECASE)
    return webPage_regex.findall(html)


def get_robots(url):
    rp = robotparser.RobotFileParser()
    rp.set_url(urlparse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


if __name__ == '__main__':
    # link_crawler('http://example.webscraping.com', '/(index|view)', scrape_callback=ScrapeCallback())
    #link_crawler('http://example.webscraping.com/', '/(index|view)', 2, 'wswp', None, ScrapeCallback(), DiskCache())
    link_crawler('http://www.resgain.net/english_names_z_1.html', '/english_names_[a-z]_[0-9]{0,3}.html', user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER', scrape_callback=ScrapeCallback())
    print 'finished'
