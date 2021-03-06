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

class A3gscSpider(scrapy.Spider):
    name = '3gsc'
    allowed_domains = ['www.3gsc.com.cn']
    start_urls = []
    lists = [
        'http://www.3gsc.com.cn/book/235614'
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,======================',response.url)
        text = response.text
        # print(text)
        item = TNovelItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h1[@class="RecArticle"]//text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P30'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        author = ''.join(response.xpath('//span[@class="RecAuthor fl"]/a[@class="author"]/text()').extract()).strip()
        item["author"] = author
        print('author:', author)
        novel_type = ';'.join(response.xpath('//div[@class="rec_con rec_con_2"]/div[@class="RecReview1"]/ul/li/a[@class="Sort"]/text()').extract()).strip()
        item["novel_type"] = novel_type
        print('novel_type:', novel_type)
        tags_s = ';'.join(response.xpath('//p[@class="showmore"]/a/text()').extract()).strip()
        if '、' in tags_s:
            tags = tags_s.replace('、', ';')
        else:
            tags = tags_s
        item["tags"] = tags
        print('tags:', tags)
        Signed = ''.join(response.xpath('//div[@class="icon-recommend pa"]/@style').extract()).strip()
        print('Signed:',Signed)
        # if '签约作品' in Signed:
        #     Signed = 1
        # else:
        #     Signed = 0
        item["Signed"] = Signed
        # print('Signed:', Signed)
        novel_desc = ''.join(response.xpath('//div[@class="RecReview RecReview_one"]/text()').extract()).strip()
        item["novel_desc"] = novel_desc
        print('novel_desc:', novel_desc)
        Product_image = plat_number + product_number
        Product_image = hashlib.md5(Product_image.encode(encoding='UTF-8')).hexdigest()
        print('Product_image:', Product_image)
        item["Product_image"] = Product_image
        P_image = ''.join(response.xpath('//div[@class="RecBook fl"]/a/img/@src').extract()).strip()
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