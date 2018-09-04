# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
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


class ShuqiSpider(scrapy.Spider):
    name = 'shuqi'
    allowed_domains = ['http://www.shuqi.com/']
    start_urls = []
    lists = [
        'http://www.shuqi.com/cover.php?bid=12276'
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=======================', response.url)
        # print(response.text)
        # url = response.url
        item = TNovelSummaryItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        bid = response.url.replace('http://www.shuqi.com/cover.php?bid=', '')
        print('bid:', bid)
        timestamp = str(int(time.time()))[0:10]
        print('timestamp:', timestamp)
        pageKey = "f2850e634f85f485d719314ae3cfe252"
        # jsstr = self.get_js()
        # ctx = execjs.compile(jsstr)
        s = bid + timestamp + pageKey
        sign = hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()
        print('sign:', sign)
        formdata = {
            'bid': bid,
            'timestamp': timestamp,
            'sign': sign,
        }
        link = 'https://ognv1.sqreader.com/index.php?r=pcapi/pcbook/bookinfo'
        yield scrapy.FormRequest(
            url=link,
            formdata=formdata,
            callback=self.parse_page_p,
            meta={'bid': bid, 'item': item},
            dont_filter=True,
        )

    def parse_page_p(self, response):
        print('2,=======================', response.url)
        item = response.meta["item"]
        text = response.text
        # print(response.text)
        jsons = json.loads(text)
        # print(jsons)
        data = jsons.get('data')
        # print(data)
        product_number = data.get('book_name')
        if '【' and '】' in product_number:
            product_number = product_number.replace('【', '[').replace('】', ']')
            print('product_number:', product_number)
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
        else:
            product_number = product_number
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
        plat_number = 'P19'
        item["plat_number"] = plat_number
        print('plat_number:', plat_number)
        Chapter_num_update = data.get('newChapName')
        Chapter_num_update = ''.join(re.findall(r'\d+',Chapter_num_update))
        item["Chapter_num_update"] = Chapter_num_update
        print('Chapter_num_update:',Chapter_num_update)
        update_date = data.get('up_time')
        update_date = time.localtime(int(update_date))
        update_date = time.strftime("%Y-%m-%d %H:%M:%S", update_date)
        item["update_date"] = update_date
        print('update_date:',update_date)
        words = data.get('size')
        item["words"] = words
        print('words:',words)
        click_num = None
        item["click_num"] = click_num
        print('click_num:',click_num)
        tickets_num = None
        item["tickets_num"] = tickets_num
        print('tickets_num:',tickets_num)
        score = None
        item["score"] = score
        print('score:',score)
        collect_num = None
        item["collect_num"] = collect_num
        print('collect_num:',collect_num)
        reward_num = None
        item["reward_num"] = reward_num
        print('reward_num:',reward_num)
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        sqBid = data.get('sqBid')
        print('sqBid:', sqBid)
        bookId = sqBid
        sqAuthorId = data.get('sqAuthorId')
        print('sqAuthorId:', sqAuthorId)
        authorId = sqAuthorId
        link = 'https://read.xiaoshuo1-sm.com/novel/i.php?do=sp_get&authorId={}&bookId={}&fetch=merge&source=store&sqUid=1021116080'.format(
            authorId, bookId)
        yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item}, dont_filter=True)
    def parse_page(self,response):
        print('3,===================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(response.text)
        jsons = json.loads(text)
        # print(jsons)
        comment_num = jsons.get('info').get('total')
        item["comment_num"] = comment_num
        print('comment_num:',comment_num)
        print('item:',item)
        yield item