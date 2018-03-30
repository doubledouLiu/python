__author__ = 'liudoudou'
import os
import json
import pprint
import urllib
import urllib2
import lxml.html
import cookielib

LOGIN_EMAIL = '18320781961'
LOGIN_PASSWORD = 'doudou240703!!'
LOGIN_URL = 'http://www.iqiyi.com/iframe/loginreg'


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def login_cookies():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encoded_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL, encoded_data)
    response = opener.open(request)
    print response.geturl()
    return opener


def login_test():
    html = urllib2.urlopen(LOGIN_URL).read()
    form = parse_form(html)
    pprint.pprint(form)


if __name__ == '__main__':
    login_test()

