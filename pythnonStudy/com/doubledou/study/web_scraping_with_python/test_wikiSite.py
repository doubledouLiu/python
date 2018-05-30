##-*- coding: utf-8 -*-
__author__ = 'liudoudou'
from urllib2 import urlopen, URLError, HTTPError
from bs4 import BeautifulSoup
import datetime
import random
import re

random.seed(datetime.datetime.now())

global pages


def getWholeLinks(pageUrl):
    pages = set()
    try:
        html = urlopen("https://en.wikipedia.org" + pageUrl)
    except(HTTPError, URLError) as e:
        return None
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id="mw-content-text").findAll("p")[0])
        print(bsObj.find(id="mp-left").find("a").attrs['href'])
    except AttributeError:
        print("page lack some attributes! but do not worry")
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                newPage = link.attrs['href']
                print("\n new page: " + newPage)
                pages.add(newPage)
                getWholeLinks(newPage)


def getLinks(articleUrl):
    try:
        html = urlopen("https://en.wikipedia.org" + articleUrl)
    except(HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html,"html.parser")
        return bsObj.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
    except AttributeError as e:
        return None

if __name__ == '__main__':
    # links = getLinks("/wiki/Kevin_Bacon")
    # while len(links) > 0:
    #     newArticle = links[random.randint(0, len(links) - 1)].attrs["href"]
    #     print newArticle
    #     links = getLinks(newArticle)

    getWholeLinks("")