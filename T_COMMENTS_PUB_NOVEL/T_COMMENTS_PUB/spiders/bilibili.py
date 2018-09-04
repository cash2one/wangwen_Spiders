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

class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com']
    start_urls = []
    base_urls = ''
    lists = [
        'https://www.bilibili.com/video/av2683903?t=223',
        'https://www.bilibili.com/video/av5818395',
        'https://www.bilibili.com/video/av6606796',
        'https://www.bilibili.com/video/av5818600',
        'https://www.bilibili.com/video/av13194689',
        'https://www.bilibili.com/video/av13092384',
        'https://www.bilibili.com/video/av13093964/?p=1',
        'https://www.bilibili.com/video/av13116842',
        'https://www.bilibili.com/video/av13108441',
        'https://www.bilibili.com/video/av13091721',
        'https://www.bilibili.com/video/av13095987',
        'https://www.bilibili.com/video/av13219927',
        'https://www.bilibili.com/video/av12894495',
        'https://www.bilibili.com/video/av13108441',
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=========================',response.url)
        item = TCommentsPubItem()
        src_url = response.url
        item["src_url"] = src_url
        # print('src_url:', src_url)
        product_number = ''.join(re.findall(r'av\d+',src_url))
        # print('product_number:',product_number)
        item["product_number"] = product_number
        html = response.text
        # print(html)
        cid = ''.join(re.findall(r'cid=(\d+)&amp',html))
        # print('cid:',cid)
        link = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(cid)
        # print('link:',link)
        yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item}, dont_filter=True)
    def parse_page(self, response):
        print('2,=========================',response.url)
        text = response.text
        # print(text)
        responses = etree.HTML(text.encode('utf-8'))
        print(type(responses))
        danmu_data = re.findall(r'<d p="(.*?)">(.*?)</d>',text)
        # print(danmu_data)
        for data in danmu_data:
            # print(data)
            item = response.meta["item"]
            comments = data[1]
            item["comments"] = comments
            print('comments:',comments)

            cmt_date = data[0].split(',')[4]
            timeArray = time.localtime(int(cmt_date))
            cmt_date = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            item["cmt_date"] = cmt_date
            print('cmt_date:',cmt_date)

            cmt_time = data[0].split(',')[4]
            timeArray = time.localtime(int(cmt_time))
            cmt_time = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            item["cmt_time"] = cmt_time
            print('cmt_time:',cmt_time)

            plat_number = None
            item["plat_number"] = plat_number
            nick_name = None
            item["nick_name"] = nick_name
            like_cnt = None
            item["like_cnt"] = like_cnt
            cmt_reply_cnt = None
            item["cmt_reply_cnt"] = cmt_reply_cnt
            long_comment = None
            item["long_comment"] = long_comment
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            print('item:',item)
            yield item





