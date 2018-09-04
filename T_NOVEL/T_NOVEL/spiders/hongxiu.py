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


class HongxiuSpider(scrapy.Spider):
    name = 'hongxiu'
    allowed_domains = ['www.hongxiu.com']
    start_urls = [
        'https://www.hongxiu.com/book/8263527304935303'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 0.5})

    def parse(self, response):
        print('1,=========================',response.url)
        text = response.text
        # print(text)
        item = TNovelItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h1/em/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P33'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        author = ''.join(response.xpath('//h1/a[@class="writer default"]/text()').extract()).strip().replace('著','')
        item["author"] = author
        print('author:', author)
        novel_type = ';'.join(response.xpath('//p[@class="tag-box"]/span/i[position()>3]/text()').extract()).strip()
        item["novel_type"] = novel_type
        print('novel_type:', novel_type)
        tags = None
        item["tags"] = tags
        Signed_s = ''.join(response.xpath('//p[@class="tag-box"]/span/i/text()').extract()).strip()
        if '签约' in Signed_s:
            Signed = 1
        else:
            Signed = 0
        item["Signed"] = Signed
        print('Signed:', Signed)
        novel_desc = ''.join(response.xpath('//div[@class="book-information cf"]/div[@class="book-info"]/p[@class="intro"]/text()').extract()).strip()
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




