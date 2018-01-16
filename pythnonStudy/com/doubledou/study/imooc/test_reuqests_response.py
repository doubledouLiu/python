import requests
"""
download image or file
"""


def download_image():
    url = "https://gss2.bdstatic.com/-fo3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268%3Bg%3D0/sign=a3b2d7f0a086c9170803553ff10617f2/0df3d7ca7bcb0a46c467b8316c63f6246b60af74.jpg"
    response = requests.get(url, stream=True)
    with open('demo.jpg', 'wb') as fd:
        for chunk in response.iter_content(128):
            fd.write(chunk)
    print response.status_code


def download_image_improved():
    url = "https://gss2.bdstatic.com/-fo3dSag_xI4khGkpoWK1HF6hhy/baike/w%3D268%3Bg%3D0/sign=a3b2d7f0a086c9170803553ff10617f2/0df3d7ca7bcb0a46c467b8316c63f6246b60af74.jpg"

    from contextlib import closing
    with closing(requests.get(url, stream=True)) as response:
        with open('demo1.jpg', 'wb') as fd:
            for chunk in response.iter_content(128):
                fd.write(chunk)


if __name__ == '__main__':
    download_image_improved()
