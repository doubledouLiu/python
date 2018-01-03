import os
import json
import urllib
import urllib2
import lxml.html
import cookielib
import pprint
import time
import glob




LOGIN_EMAIL = '985389571@qq.com'
LOGIN_PASSWORD = 'doudou240703!!'
LOGIN_URL = 'http://example.webscraping.com/user/login'
COUNTRY_URL = 'http://example.webscraping.com'


def login_basic():
    data = {'email': LOGIN_EMAIL, 'password': LOGIN_PASSWORD}
    encoded_data = urllib.urlcode(data)
    request = urllib2.Request(LOGIN_URL, encoded_data)
    response = urllib2.urlopen(request)
    print response.geturl()


def parse_form(html):
    tree = lxml.html.fromstring(html)
    data = {}
    for e in tree.cssselect('form input'):
        if e.get('name'):
            data[e.get('name')] = e.get('value')
    return data


def login_formkey():
    html = urllib2.urlopen(LOGIN_URL).read()
    data = parse_form(html)
    data['email'] = LOGIN_EMAIL
    data['password'] = LOGIN_PASSWORD
    encode_data = urllib.urlencode(data)
    request = urllib2.Request(LOGIN_URL, encode_data)
    response = urllib2.urlopen(request)
    print response.geturl()


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


def login_firefox_sessions(session_filename):
    cj = cookielib.CookieJar()
    if os.path.exists(session_filename):
        try:
            json_data = json.loads(open(session_filename, 'rb').read())
        except ValueError as e:
            print 'Error parsing session Json:', str(e)
        else:
            for window in json_data.get('windows', []):
                for cookie in window.get('cookies', []):
                    pprint.pprint(cookie)
                    c = cookielib.Cookie(0, cookie.get('name', ''), cookie.get('value', ''), None, False,
                                         cookie.get('host', ''), cookie.get('host', '').startswith('.'),
                                         cookie.get('host', '').startswith('.'), cookie.get('path', ''), False,
                                         False, str(int(time.time()) + 3600 * 24 * 7), False, None, None, {})
                    cj.set_cookie(c)
    else:
        print 'Session filename does not exist:', session_filename
    return cj


def find_firefox_sessions():
    paths = [
        '~/.mozilla/firefox/*.default',
        '~/Library/Application Support/Firefox/Profiles/*.default',
        'C:\Users\liudoudou\AppData\Roaming\Mozilla\Firefox\Profiles\dnit339z.default-1467723531306\\'
    ]
    for path in paths:
        filename = os.path.join(path, 'sessionstore.js')
        matches = glob.glob(os.path.expanduser(filename))
        if matches:
            return matches[0]


def login_firefox():
    session_filename = find_firefox_sessions()
    cj = login_firefox_sessions(session_filename)
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    html = opener.open(COUNTRY_URL).read()
    tree = lxml.html.fromstring(html)
    print tree.cssselect('ul#navbar li a')[0].text_content()
    return opener


if __name__ == '__main__':
    #login_basic()
    #login_formkey()
    #login_cookies()
    login_firefox()
