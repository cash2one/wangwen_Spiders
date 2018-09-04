# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL.items import TNovelItem
from T_NOVEL.utils.get_product_number import get_product_number
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


    def parse(self, response):
        print('1,=======================',response.url)
        # print(response.text)
        # url = response.url
        item = TNovelItem()
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

        author = data.get('author_name')
        print('author:',author)
        item["author"] = author
        novel_type = data.get('class_name')
        print('novel_type:',novel_type)
        item["novel_type"] = novel_type
        tags = None
        print('tags:',tags)
        item["tags"] = tags
        Signed = data.get('is_end_write')
        item["Signed"] = Signed
        print('Signed:', Signed)
        novel_desc = data.get('description')
        print('novel_desc:',novel_desc)
        item["novel_desc"] = novel_desc
        Product_image = plat_number + product_number
        Product_image = hashlib.md5(Product_image.encode(encoding='UTF-8')).hexdigest()
        print('Product_image:', Product_image)
        item["Product_image"] = Product_image
        P_image =  data.get('cover')
        print('P_image:',P_image)
        root = "../images//"
        path = root + Product_image
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                r = requests.get(P_image)
                r.raise_for_status()
                # 使用with语句可以不用自己手动关闭已经打开的文件流存储本地
                with open(path, "wb") as f:  # 开始写文件，wb代表写二进制文件
                    f.write(r.content)
                print("图片本地存储完成")
            else:
                print("文件已存在")
        except Exception as e:
            print("图片本地存储失败:" + str(e))
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)


