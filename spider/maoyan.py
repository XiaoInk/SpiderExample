# -*- coding: utf-8 -*-
"""
    Created by XiaoInk at 2021/2/22 01:17
    GitHub: https://github.com/XiaoInk
"""

import argparse
import logging

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO)
INDEX_URL = 'https://maoyan.com/'
TOP100_URL = 'https://maoyan.com/board/4?offset={offset}'


class MaoYan(object):

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
        }
        self.cookies = None
        self.request(INDEX_URL)  # 获取cookies

    def top100(self, offset: int = 0, limit: int = 1):
        while True:
            r = self.request(TOP100_URL.format(offset=offset))
            logging.info(f'current url <{r.url}> HTTP code <{r.status_code}>')
            if r.status_code == 200:
                html = r.text.encode(r.encoding).decode('utf8')
                soup = BeautifulSoup(html, 'html5lib')
                dds = soup.find('dl', attrs={'class': 'board-wrapper'}).find_all('dd')
                for item in dds:
                    a = item.select_one('a')
                    print({
                        'id': a.get('href').split('/')[-1],
                        'title': a.get('title'),
                        'image': a.find('img', attrs={'class': 'board-img'}).get('data-src').split('@')[0]
                    })

                offset += len(dds)
                if offset >= limit * len(dds): break
            else:
                logging.warning(f'HTTP code <{r.status_code}> error <{r.reason}>')
                break

    def request(self, url: str) -> requests.Response:
        r = requests.get(url, headers=self.headers, cookies=self.cookies)
        if self.cookies is None: self.cookies = r.cookies
        return r


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', dest='offset', type=int, default=0, help='starting point')
    parser.add_argument('-l', dest='limit', type=int, default=1, help='end point')
    args = parser.parse_args()
    MaoYan().top100(args.offset, args.limit)
