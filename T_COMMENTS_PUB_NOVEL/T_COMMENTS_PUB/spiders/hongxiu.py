# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_COMMENTS_PUB.items import TCommentsPubItem
from T_COMMENTS_PUB.utils.get_product_number import get_product_number
#from T_NOVEL.utils.process import process_date,process_number
from scrapy_splash import SplashRequest, SplashFormRequest
# from IqiyiSpider.getItem import get_item
from scrapy_redis.spiders import RedisSpider
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
import math

class HongxiuSpider(scrapy.Spider):
    name = 'hongxiu'
    allowed_domains = ['www.hongxiu.com']
    start_urls = []
    base_urls = ''
    lists = [
        'https://www.hongxiu.com/book/8263527304935303'
    ]

    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,========================',response.url)
        item = TCommentsPubItem()
        url = response.url
        src_url = url
        item["src_url"] = src_url
        # print('src_url:', src_url)
        html = response.text
        # print(html)
        # cookies = dict(responses.cookies.items())
        # print('cookies:',cookies)
        bookId = url.replace('https://www.hongxiu.com/book/','')
        print('bookId:',bookId)
        link = 'https://www.hongxiu.com/ajax/comment/pageList?_csrfToken=9bx7F3sUwWZoBWjQrEImCBarm6KMDNYhoG8EtVSc&pageNum=1&pageSize=10&bookId={}'.format(bookId)
        yield scrapy.Request(url=link, callback=self.parse_page_link, meta={'item': item, 'bookId': bookId}, dont_filter=True)
    def parse_page_link(self, response):
        print('2,==================',response.url)
        item = response.meta["item"]
        bookId = response.meta["bookId"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print(jsons)
        total = jsons.get('data').get('total')
        # print('total:',int(total/10)+1)
        maxpage = math.ceil(total/10)
        print('maxpage:',maxpage)
        for page in range(1, int(maxpage)+1):
            link =  'https://www.hongxiu.com/ajax/comment/pageList?_csrfToken=9bx7F3sUwWZoBWjQrEImCBarm6KMDNYhoG8EtVSc&pageNum={}&pageSize=10&bookId={}'.format(page, bookId)
            yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item},dont_filter=True)
    def parse_page(self, response):
        print('3,=======================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print('jsons:',jsons)
        data = jsons.get('data')
        # print('data:',data)
        product_number = data.get('bookInfo').get('bookName')
        # product_number = get_product_number(product_number)
        # print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P33'
        # print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        threadList = data.get('threadList')
        # print('threadList:',threadList)
        for thread in threadList:
            # print('thread:',thread)
            nick_name = thread.get('userName')
            item["nick_name"] = nick_name
            # print('nick_name:',nick_name)
            cmt_date = thread.get('createTime')
            # dateTime = thread.get('dateTime')
            # print('dateTime:',dateTime)
            cmt_date = time.localtime(int(cmt_date))
            # print('cmt_date:', cmt_date)
            cmt_date = time.strftime("%Y-%m-%d", cmt_date)
            item["cmt_date"] = cmt_date
            # print('cmt_date:',cmt_date)
            cmt_time = thread.get('createTime')
            cmt_time = time.localtime(int(cmt_time))
            cmt_time = time.strftime("%Y-%m-%d %H:%M:%S", cmt_time)
            item["cmt_time"] = cmt_time
            # print('cmt_time:', cmt_time)
            comments = thread.get('content')
            item["comments"] = comments
            # print('comments:',comments)
            like_cnt = None
            item["like_cnt"] = like_cnt
            cmt_reply_cnt = thread.get('repNum')
            item["cmt_reply_cnt"] = cmt_reply_cnt
            # print('cmt_reply_cnt:',cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            # print('last_modify_date:', last_modify_date)
            print('item:',item)
            print('==============================================')
            yield item



