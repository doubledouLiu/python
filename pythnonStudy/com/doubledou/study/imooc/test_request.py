import requests
import json

URL_IP = 'http://httpbin.org/ip'
URL_GET = 'http://httpbin.org/get'
URL = 'https://api.github.com'


def use_simple_request():
    response = requests.get(URL_IP)
    print ('>>Response Headers:')
    print (response.headers)
    print ('>>>Response Body:')
    print (response.text)


def use_params_request():
    params = {'param1': 'hello','param2': 'world'}
    response = requests.get(URL_GET, params=params)
    print ('>>Response Headers:')
    print (response.headers)
    print ('>>>Status Code:')
    print (response.status_code)
    print ('>>>Response Body:')
    print (response.json())


def build_uri(endpoint):
    return '/'.join([URL, endpoint])


def better_print(json_str):
    return json.dumps(json.loads(json_str), indent=4)


def request_method():
    response = requests.get(build_uri('user/emails'), auth=('imoocdemo', 'imoocdemo123'))
    print(better_print(response.text))


def params_request():
    response = requests.get(build_uri('user'), params={'since':11})
    print (better_print(response.text))
    print(response.headers)
    print(response.url)


if __name__ == '__main__':
    params_request()