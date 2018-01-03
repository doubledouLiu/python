from io import BytesIO
import lxml.html
import lxml.etree
import lxml.t
import urllib2
import urllib

REGISTER_URL = 'http://example.webscraping.com/user/register'


def extract_image(html):
    tree = lxml.html.fromstring(html)
    img_data = tree.cssselect('div#recaptcha img')[0].get('src')


def test(url):
    lxml.etree
    tree = lxml.etree.parse(url)
