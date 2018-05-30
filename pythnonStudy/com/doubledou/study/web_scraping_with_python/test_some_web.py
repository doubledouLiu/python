##-*- coding: utf-8 -*-
__author__ = 'liudoudou'
from urllib.request import Request, urlopen, URLError, HTTPError
from urllib.parse import urlparse
import ssl
from bs4 import BeautifulSoup
import re
import datetime
import random


pages = set()
random.seed(datetime.datetime.now())


#获取页面所有内链的列表
def getInternalLinks(bsObj, includeUrl):
    includeUrl = urlparse(includeUrl).scheme + "://" + urlparse(includeUrl).netloc
    internalLinks = []
    #找出所有以"/"开头或是全地址的链接
    for link in bsObj.findAll("a", href=re.compile("^(/|.*" + includeUrl + ")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                if link.attrs['href'].startswith("/"):
                    internalLinks.append(includeUrl + link.attrs['href'])
                else:
                    internalLinks.append(link.attrs['href'])

    return internalLinks


#获取页面所有的外链的列表
def getExternalLinks(bsObj, excludeUrl):
    externalUrls = []
    #找到所有以"http"或"www"开头且不包含当前url的链接
    for link in bsObj.findAll("a", href=re.compile("^(http|https)((?!" + excludeUrl + ").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalUrls:
                externalUrls.append(link.attrs['href'])

    return externalUrls


#分割http地址
def splitAddress(address):
    addressParts = address.replace("http://","").split("/")
    return addressParts


#获取随机的网页外链的列表
def getRandomExternalLinks(startingPage):
    context = ssl._create_unverified_context()
    html = urlopen(startingPage, context=context)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, urlparse(startingPage).netloc)
    if len(externalLinks) == 0:
        print("No external links looking around the site for one")
        domain = urlparse(startingPage).scheme + "://" + urlparse(startingPage).netloc
        internalLinks = getInternalLinks(bsObj, domain)
        return getRandomExternalLinks(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]



#只获取随机的外链的连接
def followExternalOnly(startingSite):
    externalLink = getRandomExternalLinks(startingSite)
    print("Random external link is:" + externalLink)
    followExternalOnly(externalLink)

#收集网站上发现的所有外链列表
allExtLinks = set()
allIntLinks = set()
def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html)
    internalLinks = getInternalLinks(bsObj, splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bsObj, splitAddress(siteUrl)[0])
    for link in externalLinks:
        allExtLinks.add(link)
        print(link)
    for link in internalLinks:
        if link not in allIntLinks:
            print("the next link to get is :" + link)
            allIntLinks.add(link)
            getAllExternalLinks(link)

if __name__ == '__main__':

    followExternalOnly("http://oreilly.com")
    getAllExternalLinks("http://oreilly.com")


