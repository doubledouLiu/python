from datetime import datetime, timedelta
from pymongo import MongoClient
import time
import zlib
import pickle
from bson.binary import Binary


class MongoCache:
    def __init__(self, client=None, expires=timedelta(days=30)):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client.cache
        self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id': url})
        if record:
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + 'does not exist')

    def __setitem__(self, url, result):
        record = {'result': Binary(zlib.compress(pickle.dumps(result))), 'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)


if __name__ == '__main__':
    cache = MongoCache(expires=timedelta())
    url = 'http://example.webscraping.com/'
    result = {'html': '...'}
    cache[url] = result
    print cache[url]
    time.sleep(60)
    print cache[url]
