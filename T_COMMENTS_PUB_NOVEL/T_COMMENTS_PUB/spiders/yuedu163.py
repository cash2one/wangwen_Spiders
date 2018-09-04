# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_COMMENTS_PUB.items import TCommentsPubItem
from T_COMMENTS_PUB.utils.get_product_number import get_product_number
from T_COMMENTS_PUB.utils.process import process_date,process_number,parse_date
from scrapy_splash import SplashRequest, SplashFormRequest
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

class Yuedu163Spider(scrapy.Spider):
    name = 'yuedu163'
    allowed_domains = ['yuedu.163.com']
    start_urls = []
    lists = [
        'http://yuedu.163.com/source/a798a334c1cd4445beeba9fc262a9735_4'
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,==========================',response.url)
        # print(response.text)
        item = TCommentsPubItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h3[@title]/em/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P34'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        bookid = ''.join(re.findall(r'source\/(.*)', src_url, re.I | re.M))
        link = 'http://yuedu.163.com/snsComment.do?operation=get&type=2&id={}&page=1'.format(bookid)
        yield scrapy.Request(url=link, callback=self.parse_page_max, meta={'item': item, 'bookid': bookid},dont_filter=True)

    def parse_page_max(self, response):
        print('2,===========================',response.url)
        item = response.meta["item"]
        bookid = response.meta["bookid"]
        text = response.text
        jsons = json.loads(text)
        # print(jsons)
        max_page = jsons.get('totalPage')
        print('max_page:',max_page)
        for page in range(1, int(max_page)+1):
            link = 'http://yuedu.163.com/snsComment.do?operation=get&type=2&id={}&page={}'.format(bookid, page)
            yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item},dont_filter=True)
    def parse_page(self, response):
        print('3,===========================',response.url)
        item = response.meta["item"]
        jsons = json.loads(response.text)
        # print(jsons)
        datas = jsons.get("data")
        # print(datas)
        for data in datas:
            # print(data)
            nick_name = data.get('username')
            item["nick_name"] = nick_name
            print('nick_name:',nick_name)
            cmt_date = data.get('posttime')
            cmt_date = parse_date(cmt_date)
            item["cmt_date"] = cmt_date
            print('cmt_date:',cmt_date)
            cmt_time = data.get('posttime')
            cmt_time = parse_date(cmt_time)
            item["cmt_time"] = cmt_time
            print('cmt_time:',cmt_time)
            comments = data.get('text')
            item["comments"] = comments
            print('comments:',comments)
            like_cnt = data.get('likes')
            item["like_cnt"] = like_cnt
            print('like_cnt:',like_cnt)
            cmt_reply_cnt = data.get('self')
            item["cmt_reply_cnt"] = cmt_reply_cnt
            print('cmt_reply_cnt:',cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            print('long_comment:',long_comment)
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            print('last_modify_date:', last_modify_date)

            print(item)
            yield item







