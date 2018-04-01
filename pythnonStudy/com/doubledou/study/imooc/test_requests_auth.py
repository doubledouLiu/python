import requests
BASE_URL = 'https://api.github.com'


def construct_url(end_point):
    return '/'.join([BASE_URL, end_point])


def base_auth():
    response = requests.get(construct_url('user'), auth=('imoocdemo', 'imoocdemo123'))
    print(response.text)
    print(response.request.headers)


def base_oauth():
    headers = {'Authorization': 'token b4b851533994c2bba1d42f7a78ba2def946a66c0'}
    response = requests.get(construct_url('user/emails'), headers=headers)
    print(response.request.headers)
    print(response.text)
    print(response.status_code)


from requests .auth import AuthBase


class GithubAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = ' '.join(['token', self.token])
        return r


def oauth_advanced():
    auth = GithubAuth('b4b851533994c2bba1d42f7a78ba2def946a66c0')
    response = requests.get(construct_url('user/emails'), auth=auth)
    print(response.text)


if __name__ == '__main__':
    #base_oauth('b4b851533994c2bba1d42f7a78ba2def946a66c0')
    oauth_advanced()

