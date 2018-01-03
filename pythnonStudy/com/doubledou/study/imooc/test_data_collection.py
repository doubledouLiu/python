import urllib2
from urllib import urlencode
req = urllib2.Request("https://www.baidu.com/")
req.add_header("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36")
resp = urllib2.urlopen(req)
print (resp.read().decode("utf-8"))