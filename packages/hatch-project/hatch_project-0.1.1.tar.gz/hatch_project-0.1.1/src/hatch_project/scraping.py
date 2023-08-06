# scraping.py
import time

from bs4 import BeautifulSoup as bs4
import requests

class Scp(object):

    def set_url_and_tag(self, url, tag, attrs={}):

        if 'https://' not in url:
            raise ValueError(
                    'Invalid URL:Example is https://example.com/.')

        time.sleep(1)
        request = requests.get(url)
        soup = bs4(request.content, 'html.parser')
        value = soup.find_all(tag, attrs=attrs)
        datas = []

        for val in value:
            datas.append(val.text)
        return datas
