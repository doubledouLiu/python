import os
import re
import urlparse
import pickle
from datetime import datetime, timedelta
import zlib


class DiskCache:
    def __init__(self, cache_dir='cache', max_length=1):
        self.cache_dir = cache_dir
        self.max_length = max_length

    def url_to_path(self, url):
        components = urlparse.urlsplit(url)
        path = components.path
        if not path:
            path = '/index.txt'
        elif path.endswith('/'):
            path += 'index.txt'
        if not path.endswith('txt'):
            path += '.txt'
        filename = components.netloc + path + components.query
        filename = re.sub('[^/0-9a-zA-Z\-.,;_ ]', '_', filename)
        filename = '/'.join(segment[:255] for segment in filename.split('/'))
        return os.path.join(self.cache_dir, filename)

    def __getitem__(self, url):
        path = self.url_to_path(url)
        if os.path.exists(path):
            with open(path, 'rb') as fp:
                data = fp.read()
                data = zlib.decompress(data)
                result, timestamp = pickle.loads(data)
                return result
        else:
            raise KeyError(url + 'does not exist')

    def __setitem__(self, url, result):
        path = self.url_to_path(url)
        folder = os.path.dirname(path)
        if not os.path.exists(folder):
            os.makedirs(folder)
        data = pickle.dumps((result, datetime.utcnow()))
        data = zlib.compress(data)
        with open(path, 'wb') as fp:
            fp.write(data)