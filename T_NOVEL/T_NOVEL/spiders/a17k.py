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

class A17kSpider(scrapy.Spider):
    name = '17k'
    allowed_domains = ['http://www.17k.com']
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
        print('1,================',response.url)
        # print(response.text)
        item = TNovelItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//div[@class="Info Sign"]/h1/a[@target="_blank"]/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P22'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        author = ''.join(response.xpath('//div[@class="author"]/a[@class="name"]/text()').extract()).strip()
        item["author"] = author
        print('author:',author)
        novel_type = ''.join(response.xpath('//dl[@class="Tab"]/dd/div[2]/table/tr[1]/td/a/text()').extract()).strip()
        item["novel_type"] = novel_type
        print('novel_type:',novel_type)
        tags_s = ';'.join(response.xpath('//dl[@class="Tab"]/dd/div[2]/table/tr[last()]/td/a/span/text()').extract()).strip()
        if '、' in tags_s:
            tags = tags_s.replace('、',';')
        else:
            tags = tags_s
        item["tags"] = tags
        print('tags:',tags)
        Signed = ''.join(response.xpath('//dl[@class="Tab"]/dd/div[2]/table/tr[1]/td/span/text()').extract()).strip()
        # print('Signed:',Signed)
        if '签约作品' in Signed:
            Signed = 1
        else:
            Signed = 0
        item["Signed"] = Signed
        print('Signed:',Signed)
        novel_desc = ''.join(response.xpath('//dl[@class="Tab"]/dd/div[1]/a//text()').extract()).strip()
        item["novel_desc"] = novel_desc
        print('novel_desc:',novel_desc)
        Product_image = plat_number + product_number
        Product_image = hashlib.md5(Product_image.encode(encoding='UTF-8')).hexdigest()
        print('Product_image:', Product_image)
        item["Product_image"] = Product_image
        P_image = ''.join(response.xpath('//div[@id="bookCover"]/a/img/@src').extract()).strip()
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