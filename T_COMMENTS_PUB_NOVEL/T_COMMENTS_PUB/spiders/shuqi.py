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


class ShuqiSpider(scrapy.Spider):
    name = 'shuqi'
    allowed_domains = ['www.shuqi.com/']
    start_urls = []
    lists = [
        'http://www.shuqi.com/cover.php?bid=12276'
    ]
    for l in lists:
        start_urls.append(l)

    # 获取js内容
    def get_js(self):
        # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
        f = open("./js/shuqi_js.js", 'r', encoding='UTF-8')
        line = f.readline()
        htmlstr = ''
        while line:
            htmlstr = htmlstr + line
            line = f.readline()
        return htmlstr

    def parse(self, response):
        print('1,=====================',response.url)
        # print(response.text)
        url = response.url
        item = TCommentsPubItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        bid = response.url.replace('http://www.shuqi.com/cover.php?bid=','')
        print('bid:',bid)
        timestamp = str(int(time.time()))[0:10]
        print('timestamp:',timestamp)
        pageKey = "f2850e634f85f485d719314ae3cfe252"
        # jsstr = self.get_js()
        # ctx = execjs.compile(jsstr)
        s = bid + timestamp + pageKey
        sign = hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()
        print('sign:',sign)
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
            meta={'bid': bid,'item': item},
            dont_filter=True,
        )

    def parse_page_p(self, response):
        print('2,=======================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(response.text)
        jsons = json.loads(text)
        # print(jsons)
        data = jsons.get('data')
        # print('data:',data)
        product_number = data.get('book_name')
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P21'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        sqBid = data.get('sqBid')
        print('sqBid:',sqBid)
        bookId = sqBid
        sqAuthorId = data.get('sqAuthorId')
        print('sqAuthorId:',sqAuthorId)
        authorId = sqAuthorId
        link = 'https://read.xiaoshuo1-sm.com/novel/i.php?do=sp_get&authorId={}&bookId={}&fetch=merge&source=store&sqUid=1021116080'.format(authorId, bookId)
        yield scrapy.Request(url=link, callback=self.parse_page_link, meta={'item': item,'bookId':bookId,'authorId':authorId},dont_filter=True)
    def parse_page_link(self, response):
        print('3,==================',response.url)
        item = response.meta["item"]
        bookId = response.meta["bookId"]
        authorId = response.meta["authorId"]
        text = response.text
        # print(response.text)
        jsons = json.loads(text)
        # print(jsons)
        maxpage = jsons.get('info').get('count')
        print('maxpage:',maxpage)
        for page in range(1, int(maxpage)+1):
            link = 'https://read.xiaoshuo1-sm.com/novel/i.php?do=sp_get&authorId={}&bookId={}&fetch=merge&source=store&sqUid=1021116080&page={}'.format(authorId, bookId, page)
            yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item}, dont_filter=True)
    def parse_page(self,response):
        print('4,======================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print(jsons)
        data = jsons.get('data')
        for d in data:
            # print(d)
            nick_name = d.get('nickName')
            item["nick_name"] = nick_name
            # print('nick_name:',nick_name)
            cmt_date = d.get('pubTime')
            cmt_date = time.localtime(int(cmt_date))
            cmt_date = time.strftime("%Y-%m-%d", cmt_date)
            item["cmt_date"] = cmt_date
            # print('cmt_date:',cmt_date)
            cmt_time = d.get('pubTime')
            cmt_time = time.localtime(int(cmt_time))
            cmt_time = time.strftime("%Y-%m-%d %H:%M:%S", cmt_time)
            item["cmt_time"] = cmt_time
            # print('cmt_time:', cmt_time)
            comments = d.get('text')
            item["comments"] = comments
            # print('comments:',comments)
            like_cnt = d.get('zanNum')
            item["like_cnt"] = like_cnt
            # print('like_cnt:',like_cnt)
            cmt_reply_cnt = d.get('replyNum')
            item["cmt_reply_cnt"] = cmt_reply_cnt
            # print('cmt_reply_cnt:',cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            print('item:',item)
            yield item



