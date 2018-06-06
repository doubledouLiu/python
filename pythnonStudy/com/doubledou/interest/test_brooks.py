##-*- coding: utf-8 -*-
__author__ = 'liudoudou'
import urllib
from bs4 import BeautifulSoup
import json

availableUrl = "http://www.brooksbrothers.com/on/demandware.store/Sites-brooksbrothers-Site/default/Product-GetAvailability?format=ajax&pid="


def getProductDetail(detailUrl):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        req = urllib.request.Request(url=detailUrl, headers=headers)
        html = urllib.request.urlopen(req)
    except Exception as e:
        print(e)
        return None

    try:
        bsObj = BeautifulSoup(html)

        #提取商品名称
        name = bsObj.find(id="product-content").find("h1").get_text()
        print(name)
        #提取商品id
        productId = bsObj.find(id="product-content").find(attrs={'class', 'product-number'}).find("span").get_text()
        print(productId)
        #提取商品价格
        price = bsObj.find(id="product-content").find(attrs={'class', 'price-value'}).get_text()
        print(price)
        #提取商品简介
        description = bsObj.find(id="product-content").find(attrs={'class', 'description'}).get_text()
        print(description)
        #提取商品颜色
        colors = bsObj.find(id="product-content").findAll(attrs={'class', 'swatchanchor'})
        sizes = bsObj.find(id="product-content").findAll(attrs={'class', 'size-anchor'})
        for color in colors:
            colorUrl = color.attrs['href']
            colorParam = splitAddress(colorUrl, "Color", productId)
            print(colorParam)
            for size in sizes:
                sizeUrl = size.attrs['href']
                sizeParam = splitAddress(sizeUrl, "Size", productId)
                print(sizeParam)
                stockUrl = availableUrl + productId + "_____" + colorParam + "_" + sizeParam + "_______"
                availableForSale = getProductStock(stockUrl)
                print("color : " + colorParam + " size : " + sizeParam + " is availableForSale : " + str(availableForSale))
    except AttributeError as e:
        print(e)
        return None


def getProductStock(stockUrl):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
        req = urllib.request.Request(url=stockUrl, headers=headers)
        html = urllib.request.urlopen(req)
    except(Exception) as e:
        print(e)
        return None
    try:
        dataHtml = html.read()
        dataJson = json.loads(dataHtml)
        return dataJson['availableForSale']
    except Exception as e:
        print(e)
        return None


#分割http地址
def splitAddress(address, type, productId):
    addressParts = address.split("&")
    for part in addressParts:
        if type in part:
            return part.replace(type, "").replace(productId, "").replace("_", "").replace("dwvar=", "")
    return ""


if __name__ == '__main__':
    getProductDetail("http://www.brooksbrothers.com/on/demandware.store/Sites-brooksbrothers-Site/default/Product-Variation?pid=SX00145")