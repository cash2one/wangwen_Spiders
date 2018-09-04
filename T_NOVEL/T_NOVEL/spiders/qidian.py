# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL.items import TNovelItem
from T_NOVEL.utils.get_product_number import get_product_number
from T_NOVEL.utils.process import process_date,process_number,chinesedigits
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


class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['book.qidian.com']
    start_urls = [
        'https://book.qidian.com/info/3347812',
        'https://book.qidian.com/info/3394903',
        'https://book.qidian.com/info/1009915605',
        'https://book.qidian.com/info/3347395',
        'https://book.qidian.com/info/3363928',
        'https://book.qidian.com/info/107580',
        'https://book.qidian.com/info/1887208',
        'https://book.qidian.com/info/1735921',
        'https://book.qidian.com/info/3242304',
        'https://book.qidian.com/info/1004175804',
        'https://book.qidian.com/info/1003580078',
        'https://book.qidian.com/info/3348326',
        'https://book.qidian.com/info/2048120',
        'https://book.qidian.com/info/2502372',
        'https://book.qidian.com/info/2952453',
        'https://book.qidian.com/info/2750457',
        'https://book.qidian.com/info/1005238666',
        'https://book.qidian.com/info/2413595',
        'https://book.qidian.com/info/3348312',
        'https://book.qidian.com/info/2083259',
        'https://book.qidian.com/info/2248950',
        'https://book.qidian.com/info/3358605',
        'https://book.qidian.com/info/1004179514',
        'https://book.qidian.com/info/1001579096',
        'https://book.qidian.com/info/1931432',
        'https://book.qidian.com/info/1004608738',
        'https://book.qidian.com/info/1979049',
        'https://book.qidian.com/info/1003354631',
        'https://book.qidian.com/info/1010191960',
        'https://book.qidian.com/info/1010468795#Catalog',
        'https://book.qidian.com/info/3602691',
        'https://book.qidian.com/info/1010734492',
        'https://book.qidian.com/info/1009704712',
        'https://book.qidian.com/info/3681560',
        'https://book.qidian.com/info/1010136878',
        'https://book.qidian.com/info/3258971',
        'https://book.qidian.com/info/2494758',
        'https://book.qidian.com/info/1004185492',
        'https://book.qidian.com/info/1003541158',
        'https://book.qidian.com/info/2226569',
        'https://book.qidian.com/info/1010399782',
        'https://book.qidian.com/info/1010868264',
        'https://book.qidian.com/info/1003306811',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})
    def parse(self, response):
        print('1,=====================',response.url)
        text = response.text
        # print(text)
        item = TNovelItem()
        url = response.url
        src_url = url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h1/em/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P20'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        author = ''.join(response.xpath('//h1/span/a[@class="writer"]/text()').extract()).strip()
        item["author"] = author
        print('author:', author)
        novel_type = ';'.join(response.xpath('//p[@class="tag"]/a/text()').extract()).strip()
        item["novel_type"] = novel_type
        print('novel_type:', novel_type)
        tags = None
        item["tags"] = tags
        print('tags:', tags)
        Signed = ''.join(response.xpath('//p[@class="tag"]/span[@class="blue"]/text()').extract()).strip()
        if '签约' in Signed:
            Signed = 1
        else:
            Signed = 0
        item["Signed"] = Signed
        print('Signed:', Signed)
        novel_desc = ''.join(response.xpath('//div[@class="book-intro"]/p/text() | //p[@class="intro"]/text()').extract()).strip()
        item["novel_desc"] = novel_desc
        print('novel_desc:', novel_desc)
        Product_image = plat_number + product_number
        Product_image = hashlib.md5(Product_image.encode(encoding='UTF-8')).hexdigest()
        print('Product_image:', Product_image)
        item["Product_image"] = Product_image
        P_image = 'http:' + ''.join(response.xpath('//*[@id="bookImg"]/img/@src').extract()).strip()
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

