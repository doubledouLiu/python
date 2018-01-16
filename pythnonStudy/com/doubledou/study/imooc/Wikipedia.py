import urllib
from bs4 import BeautifulSoup
import re

resp = urllib.urlopen("https://en.m.wikipedia.org/wiki/Main_Page").read().decode('utf-8')
soup = BeautifulSoup(resp, "html.parser")
listUrls = soup.findAll("a", href=re.compile("^/wiki/"))
for url in listUrls:
    if not re.search("\.jpg|JPG$",url['href']):
     print(url.get_text(), "<--->","https://en.m.wikipedia.org" + url['href'])