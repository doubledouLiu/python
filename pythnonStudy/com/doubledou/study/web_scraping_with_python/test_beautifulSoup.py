##-*- coding: utf-8 -*-
__author__ = 'liudoudou'
from urllib2 import Request, urlopen, URLError, HTTPError
from bs4 import BeautifulSoup


#获取title标签
def getTitle(url):
    try:
        html = urlopen(url)
    except(HTTPError, URLError) as e:
        return None
    try:
        bsObj = BeautifulSoup(html)
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title.get_text()


#提取标签
def extractTag(url):
    try:
        html = urlopen(url)
    except(HTTPError, URLError) as e:
        return None

    try:
        bsObj = BeautifulSoup(html)

        #根据tagName提取标签
        print(bsObj.h1)

        # 顺序打印所有人名
        nameList = bsObj.findAll("span", {"class": "green"})
        forTagPrint(nameList)
    except AttributeError as e:
        print(e)
        return None


def test_find(url):
    try:
        html = urlopen(url)
    except(HTTPError, URLError) as e:
        print(e)
        return None

    try:
        bsObj = BeautifulSoup(html)

        #测试tag参数
        titleList = bsObj.findAll({"h1", "h2"})
        forTagPrint(titleList)

        #测试attribute参数
        spanList = bsObj.findAll("span", {"class": {"green", "red"}})
        forTagPrint(spanList)

        #测试text参数
        princeList = bsObj.findAll(text="the prince")
        print(len(princeList))

        #测试keyword
        textList = bsObj.findAll(id="text")
        #forTagPrint(textList)
        print(textList[0].get_text())

    except AttributeError as e:
        print(e)


def forTagPrint(list):
    for item in list:
        print(item)
        print(item.get_text())

if __name__ == '__main__':
    # title = getTitle("http://www.pythonscraping.com/pages/page1.html")
    # if title is None:
    #     print("title is not found")
    # else:
    #     print(title)
    #
    # extractTag("http://www.pythonscraping.com/pages/warandpeace.html")

    test_find("http://www.pythonscraping.com/pages/warandpeace.html")
