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

class A17kSpider(scrapy.Spider):
    name = '17k'
    allowed_domains = ['www.17k.com']
    start_urls = []
    base_urls = ''
    lists = [
        'http://www.17k.com/book/1198584.html',
        'http://www.17k.com/book/471287.html',
        'http://www.17k.com/book/1859126.html',
        'http://www.17k.com/book/1540808.html',
        'http://www.17k.com/book/458754.html',
        'http://www.17k.com/book/1398783.html',
        'http://www.17k.com/book/1086778.html',
        'http://www.17k.com/book/1469383.html',
        'http://www.17k.com/book/1254615.html',
        'http://www.17k.com/book/1050747.html',
        'http://www.17k.com/book/1724482.html',
        'http://www.17k.com/book/753884.html',
        'http://www.17k.com/book/971117.html',
        'http://www.17k.com/book/966328.html',
        'http://www.17k.com/book/1724398.html',
        'http://www.17k.com/book/524383.html',
        'http://www.17k.com/book/1724165.html',
        'http://www.17k.com/book/2615612.html',
        'http://www.17k.com/book/686132.html',
        'http://www.17k.com/book/908353.html',
        'http://www.17k.com/book/650846.html',
        'http://www.17k.com/book/777148.html',
        'http://www.17k.com/book/450860.html',
        'http://www.17k.com/book/446704.html',
        'http://www.17k.com/book/1860363.html',
        'http://www.17k.com/book/2459058.html',
        'http://www.17k.com/book/916533.html',
        'http://www.17k.com/book/973809.html',
        'http://www.17k.com/book/554720.html',
        'http://www.17k.com/book/1352782.html',
        'http://www.17k.com/book/814433.html',
        'http://www.17k.com/book/737312.html',
        'http://www.17k.com/book/536438.html',
        'http://www.17k.com/book/2458377.html',
        'http://www.17k.com/book/1741975.html',
        'http://www.17k.com/book/632701.html',
        'http://www.17k.com/book/985912.html',
        'http://www.17k.com/book/2722533.html',
        'http://www.17k.com/book/2210699.html',
        'http://www.17k.com/book/2731559.html',
        'http://www.17k.com/book/592898.html',
        'http://www.17k.com/book/1172667.html',
        'http://www.17k.com/book/2469390.html',
        'http://www.17k.com/book/1286963.html',
        'http://www.17k.com/book/590918.html',
        'http://www.17k.com/book/2389814.html',
        'http://www.17k.com/book/631937.html',
        'http://www.17k.com/book/1538463.html',
        'http://www.17k.com/book/2272970.html',
        'http://www.17k.com/book/108821.html',
        'http://www.17k.com/book/391013.html',
        'http://www.17k.com/book/192453.html',
        'http://www.17k.com/book/83528.html',
        'http://www.17k.com/book/69646.html',
        'http://www.17k.com/book/143095.html',
        'http://www.17k.com/book/153917.html',
        'http://www.17k.com/book/64141.html',
        'http://www.17k.com/book/104997.html',
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,===============',response.url)
        item = TCommentsPubItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//div[@class="Info Sign"]/h1/a[@target="_blank"]/text()').extract()).strip()
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P22'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        link = ''.join(response.xpath('//div[@class="MORE"]/a[@id="comment_more2"]/@href').extract()).strip()
        # print('link:',link)
        yield scrapy.Request(url=link, callback=self.parse_page_link, meta={'item': item}, dont_filter=True)
    def parse_page_link(self, response):
        print('2,===================',response.url)
        item = response.meta["item"]
        html = response .text
        bookId = ''.join(re.findall(r"c\.data\.bookId\=\'\d+\'", html)).strip().replace("c.data.bookId='","").replace("'","")
        # print('bookId:',bookId)
        Request_URL = 'http://comment.17k.com/topic_list?bookId={}&page={}'.format(bookId,1)
        # print('Request_URL:',Request_URL)
        yield scrapy.Request(url=Request_URL, callback=self.parse_page_count,meta={'bookId': bookId, 'item': item}, dont_filter=True)
    def parse_page_count(self, response):
        print('3,==================',response.url)
        bookId = response.meta["bookId"]
        print('bookId:', bookId)
        item = response.meta["item"]
        text = response.text
        # print(type(text))
        jsons = json.loads(text)
        # print(type(jsons))
        pagecount = jsons.get('page').get('pagecount')
        print('pagecount:',pagecount)
        for page in range(1,int(pagecount)+1):
            # print('page:',page)
            URL = 'http://comment.17k.com/topic_list?bookId={}&page={}'.format(bookId, page)
            # print('URL:',URL)
            yield scrapy.Request(url=URL, callback=self.parse_page_result, meta={'item': item}, dont_filter=True)
    def parse_page_result(self, response):
        print('4,=========================',response.url)
        text = response.text
        # print(type(text))
        jsons = json.loads(text)
        # print(type(jsons))
        result = jsons.get('page').get('result')
        # print('result:', result)
        for res in result:
            # print(res)
            item = response.meta["item"]
            print('item:',item)
            nick_name = res.get('marks').get('nikeName')
            item["nick_name"] = nick_name
            print('nick_name:',nick_name)
            cmt_date = res.get('creationDate')
            cmt_date = time.localtime(int(cmt_date)/1000)
            cmt_date = time.strftime("%Y-%m-%d", cmt_date)
            item["cmt_date"] = cmt_date
            print('cmt_date:',cmt_date)
            cmt_time = res.get('creationDate')
            cmt_time = time.localtime(int(cmt_time)/1000)
            cmt_time = time.strftime("%Y-%m-%d %H:%M:%S", cmt_time)
            item["cmt_time"] = cmt_time
            print('cmt_time:',cmt_time)
            comments = res.get('summary')
            bq = re.compile(r'<(S*?)[^>]*>.*?|<.*? />', re.I)
            # 去掉HTML标签
            comments = bq.sub('', comments).strip()
            item["comments"] = comments
            print('comments:',comments)
            like_cnt = None
            item["like_cnt"] = like_cnt
            cmt_reply_cnt = res.get('replyCount')
            item["cmt_reply_cnt"] = cmt_reply_cnt
            print('cmt_reply_cnt:',cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            print('last_modify_date:', last_modify_date)
            print('=====================================================')
            yield item
