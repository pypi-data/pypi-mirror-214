from time import sleep

import loguru
from loguru import logger
# HTTP Method: GET(), POST()
import requests as rq
# 導入 BeautifulSoup module: 解析 HTML 語法工具
from bs4 import BeautifulSoup as BS
import requests
import time
import json
import datetime
from lxml import etree
import csv
import urllib3
from loguru import logger

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362',
}


class crawler_cnyes:

    def __init__(self, datetime_start: datetime.datetime = datetime.datetime.today(), datetime_end: datetime.datetime = datetime.datetime.today() + datetime.timedelta(days=1)):
        self.datetime_start = datetime_start
        self.datetime_end = datetime_end

        self.list_news = []

    @logger.catch
    def fetch(self):
        url = f'https://news.cnyes.com/api/v3/news/category/tw_stock?startAt={int(self.datetime_start.timestamp())}' \
              f'&endAt={int(self.datetime_end.timestamp())}&limit=50'
        logger.info(url)
        res = requests.get(url, headers)
        ret = json.loads(res.text)

        list_news = []
        for x in ret['items']['data']:
            title = x['title']
            str_dt = datetime.datetime.fromtimestamp(x['publishAt'])
            logger.info(f'{str_dt} {title}')
            list_news.append(f'{str_dt} {title}')

        return list_news

    def fetch_new(self):

        list_news_new = []
        list_new = self.fetch()
        for x in list_new:
            if x not in self.list_news:
                list_news_new.append(x)
        self.list_news = list_new

        return list_news_new


if __name__ == '__main__':

    cynes = crawler_cnyes()
    while True:
        sleep(1)
        ret = cynes.fetch_new()
        for x in ret:
            print(x)
