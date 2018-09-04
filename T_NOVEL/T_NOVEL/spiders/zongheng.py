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

class ZonghengSpider(scrapy.Spider):
    name = 'zongheng'
    allowed_domains = ['book.zongheng.com']
    start_urls = []
    base_urls = ''
    lists = [
        'http://book.zongheng.com/book/603738.html',
        'http://book.zongheng.com/book/523438.html',
        'http://book.zongheng.com/book/555035.html',
        'http://book.zongheng.com/book/568097.html',
        'http://book.zongheng.com/book/632434.html',
        'http://book.zongheng.com/book/635570.html',
        'http://book.zongheng.com/book/43467.html',
        'http://book.zongheng.com/book/682920.html',
        'http://book.zongheng.com/book/685640.html',
        'http://book.zongheng.com/book/512263.html',
        'http://book.zongheng.com/book/309318.html',
        'http://book.zongheng.com/book/457529.html',
        'http://book.zongheng.com/book/594492.html',
        'http://book.zongheng.com/book/342974.html',
        'http://book.zongheng.com/book/730066.html',
        'http://book.zongheng.com/book/510426.html',
        'http://book.zongheng.com/book/411993.html',
        'http://book.zongheng.com/book/45669.html',
        'http://book.zongheng.com/book/665301.html',
        'http://book.zongheng.com/book/401153.html',
        'http://book.zongheng.com/book/408586.html',
        'http://book.zongheng.com/book/481225.html',
        'http://book.zongheng.com/book/472101.html',
        'http://book.zongheng.com/book/431658.html',
        'http://book.zongheng.com/book/390470.html',
        'http://book.zongheng.com/book/524571.html',
        'http://book.zongheng.com/book/158432.html',
        'http://book.zongheng.com/book/688697.html',
        'http://book.zongheng.com/book/512648.html',
        'http://book.zongheng.com/book/470711.html',
        'http://book.zongheng.com/book/458842.html',
        'http://book.zongheng.com/book/189169.html',
        'http://book.zongheng.com/book/490372.html',
        'http://book.zongheng.com/book/435710.html',
        'http://book.zongheng.com/book/672340.html',
        'http://book.zongheng.com/book/47364.html',
        'http://book.zongheng.com/book/431145.html',
        'http://book.zongheng.com/book/280744.html',
        'http://book.zongheng.com/book/390021.html',
        'http://book.zongheng.com/book/251393.html',
        'http://book.zongheng.com/book/175703.html',
        'http://book.zongheng.com/book/570946.html',
        'http://book.zongheng.com/book/290053.html',
        'http://book.zongheng.com/book/525936.html',
        'http://book.zongheng.com/book/311835.html',
        'http://book.zongheng.com/book/732001.html',
        'http://book.zongheng.com/book/591444.html',
        'http://book.zongheng.com/book/69507.html',
        'http://book.zongheng.com/book/390199.html',
        'http://book.zongheng.com/book/347511.html',
        'http://book.zongheng.com/book/468543.html',
        'http://book.zongheng.com/book/472776.html',
        'http://book.zongheng.com/book/296950.html',
        'http://book.zongheng.com/book/513438.html',
        'http://book.zongheng.com/book/205411.html',
        'http://book.zongheng.com/book/121112.html',
        'http://book.zongheng.com/book/639927.html',
        'http://book.zongheng.com/book/88463.html',
        'http://book.zongheng.com/book/56579.html',
        'http://book.zongheng.com/book/568980.html',
        'http://book.zongheng.com/book/612328.html',
        'http://book.zongheng.com/book/676518.html',
        'http://book.zongheng.com/book/262883.html',
        'http://book.zongheng.com/book/720864.html',
        'http://book.zongheng.com/book/708632.html',
        'http://book.zongheng.com/book/377897.html',
        'http://book.zongheng.com/book/352542.html',
        'http://book.zongheng.com/book/646519.html',
        'http://book.zongheng.com/book/572891.html',
        'http://book.zongheng.com/book/36788.html',
        'http://book.zongheng.com/book/65189.html',
        'http://book.zongheng.com/book/578824.html',
        'http://book.zongheng.com/book/205836.html',
        'http://book.zongheng.com/book/714691.html',
        'http://book.zongheng.com/book/156062.html',
        'http://book.zongheng.com/book/450702.html',
        'http://book.zongheng.com/book/362880.html',
        'http://book.zongheng.com/book/645062.html',
        'http://book.zongheng.com/book/384410.html',

    ]

    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=========================',response.url)
        text = response.text
        # print(text)
        item = TNovelItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//div[@class="main"]/div[@class="status fl"]/h1/a/text()').extract()).strip()
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
        plat_number = 'P21'
        item["plat_number"] = plat_number
        print('plat_number:', plat_number)

        author = ''.join(response.xpath('//div[@class="main"]/div[@class="status fl"]/div[@class="booksub"]/a[@title]/text()').extract()).strip()
        print('author:', author)
        item["author"] = author
        novel_type = ''.join(response.xpath('//div[@class="main"]/div[@class="status fl"]/div[@class="booksub"]/a[last()]/text()').extract()).strip()
        # if '-' in novel_type:
        #     novel_type = novel_type.replace('-',';')
        print('novel_type:', novel_type)
        item["novel_type"] = novel_type
        tags = response.xpath('//div[@class="main"]/div[@class="status fl"]/div[@class="keyword"]/a[@title]/text()').extract()
        time.sleep(1)
        tags = ';'.join(tags)
        print('tags:', tags)
        item["tags"] = tags
        Signed = ''.join(response.xpath('//div[@class="main"]/div[@class="status fl"]/h1/em[@class="sign"]/@title').extract()).strip()
        if '签约作品' in Signed:
            Signed = 1
        else:
            Signed = 0
        item["Signed"] = Signed
        print('Signed:', Signed)
        novel_desc = response.xpath('//div[@class="main"]/div[@class="status fl"]/div[@class="info_con"]/p/text()').extract()
        novel_desc = '  '.join(''.join(novel_desc).split('\r'))
        # print(novel_desc)
        item["novel_desc"] = novel_desc
        print('novel_desc:',novel_desc)
        Product_image = plat_number + product_number
        Product_image = hashlib.md5(Product_image.encode(encoding='UTF-8')).hexdigest()
        print('Product_image:', Product_image)
        item["Product_image"] = Product_image
        P_image = ''.join(response.xpath('//div[@class="main"]/div[@class="book_cover fl"]/p/a/img[@title]/@src').extract()).strip()
        print('P_image:', P_image)
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

        yield item
