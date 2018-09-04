
# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,chinesedigits,parse_time
from T_NOVEL_SUMMARY.utils.words import get_words
from scrapy_splash import SplashRequest, SplashFormRequest
# from IqiyiSpider.getItem import get_item
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
import sqlite3
import requests
import os
from lxml import etree
import re
import json
from datetime import datetime
from selenium import webdriver
import time
import datetime
import regex
import execjs
import random
import hashlib
import socket
from fontTools.ttLib import TTFont
from parsel import Selector
from html import unescape


class QidianSpider(scrapy.Spider):
    name = 'qidian_3'
    allowed_domains = ['book.qidian.com']
    start_urls = [
        'https://book.qidian.com/ajax/comment/index?_csrfToken=HUc4mzWMTveOYkK01P9mREV04r5f0zisvnDNZl7j&bookId=1010191960&pageSize=15'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print('1,=================',response.url)
        text = response.text
        # print(text)
        a = requests.get(response.url)
        print(a.status_code)
        print(json.loads(a.text))
        with open('qidian.txt', "wb") as f:  # 开始写文件，wb代表写二进制文件
            f.write(a.content)
