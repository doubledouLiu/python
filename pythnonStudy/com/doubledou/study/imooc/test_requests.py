import requests
from requests import exceptions

URL = 'https://api.github.com'


def build_uri(endpoint):
    return '/'.join([URL, endpoint])


def timeout_request():
    try:
        response = requests.get(build_uri('user/emails'), timeout=0.1)
        response.raise_for_status()
    except exceptions.Timeout as e:
        print(e.message)
    except exceptions.HTTPError as e:
        print(e.message)
    else:
        print(response.text)
        print(response.status_code)


def hard_request():
    from requests import Request, Session
    s = Session()
    headers = {'User-Agent': 'fake1.3.4'}
    req = Request('GET', build_uri('user/emails'), auth=('imoocdemo','imoocdemo123'), headers=headers)
    prepped = req.prepare()
    print prepped.body
    print prepped.headers

    resp = s.send(prepped, timeout=5)
    print resp.status_code
    print resp.request.headers
    print resp.text


if __name__ == '__main__':
    hard_request()

