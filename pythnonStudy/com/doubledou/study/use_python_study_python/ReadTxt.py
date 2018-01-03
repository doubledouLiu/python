import urllib
import pdfminer

html = urllib.urlopen("https://en.wikipedia.org/robots.txt")
print(html.read().decode("utf-8"))
