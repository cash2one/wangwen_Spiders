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

class JjwxcSpider(scrapy.Spider):
    name = 'jjwxc'
    allowed_domains = ['www.jjwxc.net']
    start_urls = []
    base_urls = ''
    lists = [
        'http://www.jjwxc.net/onebook.php?novelid=3200611',
        'http://www.jjwxc.net/onebook.php?novelid=2368172',
        'http://www.jjwxc.net/onebook.php?novelid=2771073',
        'http://www.jjwxc.net/onebook.php?novelid=2973352',
        'http://www.jjwxc.net/onebook.php?novelid=1673146',
        'http://www.jjwxc.net/onebook.php?novelid=2228486',
        'http://www.jjwxc.net/onebook.php?novelid=2575223',
        'http://www.jjwxc.net/onebook.php?novelid=1857985',
        'http://www.jjwxc.net/onebook.php?novelid=126983',
        'http://www.jjwxc.net/onebook.php?novelid=1766288',
        'http://www.jjwxc.net/onebook.php?novelid=1787253',
        'http://www.jjwxc.net/onebook.php?novelid=254073',
        'http://www.jjwxc.net/onebook.php?novelid=2324217',
        'http://www.jjwxc.net/onebook.php?novelid=2370225',
        'http://www.jjwxc.net/onebook.php?novelid=2904277',
        'http://www.jjwxc.net/onebook.php?novelid=247098',
        'http://www.jjwxc.net/onebook.php?novelid=2241909',
        'http://www.jjwxc.net/onebook.php?novelid=2696632',
        'http://www.jjwxc.net/onebook.php?novelid=2589669',
        'http://www.jjwxc.net/onebook.php?novelid=2101216',
        'http://www.jjwxc.net/onebook.php?novelid=2961654',
        'http://www.jjwxc.net/onebook.php?novelid=2026432',
        'http://www.jjwxc.net/onebook.php?novelid=2550054',
        'http://www.jjwxc.net/onebook.php?novelid=2490315',
        'http://www.jjwxc.net/onebook.php?novelid=3176417',
        'http://www.jjwxc.net/onebook.php?novelid=2307154',
        'http://www.jjwxc.net/onebook.php?novelid=2553705',
        'http://www.jjwxc.net/onebook.php?novelid=3003621',
        'http://www.jjwxc.net/onebook.php?novelid=2829474',
        'http://www.jjwxc.net/onebook.php?novelid=2308730',
        'http://www.jjwxc.net/onebook.php?novelid=2827526',
        'http://www.jjwxc.net/onebook.php?novelid=2734828',
        'http://www.jjwxc.net/onebook.php?novelid=3109031',
        'http://www.jjwxc.net/onebook.php?novelid=3132729',
        'http://www.jjwxc.net/onebook.php?novelid=2691265',
        'http://www.jjwxc.net/onebook.php?novelid=2950794',
        'http://www.jjwxc.net/onebook.php?novelid=2614609',
        'http://www.jjwxc.net/onebook.php?novelid=2553345',
        'http://www.jjwxc.net/onebook.php?novelid=3039244',
        'http://www.jjwxc.net/onebook.php?novelid=3142278',
        'http://www.jjwxc.net/onebook.php?novelid=2911685',
        'http://www.jjwxc.net/onebook.php?novelid=3279919',
        'http://www.jjwxc.net/onebook.php?novelid=2840860',
        'http://www.jjwxc.net/onebook.php?novelid=2317366',
        'http://www.jjwxc.net/onebook.php?novelid=2672345',
        'http://www.jjwxc.net/onebook.php?novelid=2730439',
        'http://www.jjwxc.net/onebook.php?novelid=1239340',
        'http://www.jjwxc.net/onebook.php?novelid=370832',
        'http://www.jjwxc.net/onebook.php?novelid=3200611'

    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,================',response.url)
        # print(response.text)
        item = TNovelItem()
        product_number = ''.join(response.xpath('//h1[@itemprop="name"]/span/text()').extract()).strip()
        if '【' and '】' in product_number:
            product_number = product_number.replace('【','[').replace('】',']')
            print('product_number:',product_number)
            product_number = get_product_number(product_number)
            print('product_number:',product_number)
            item["product_number"] = product_number
        else:
            product_number = product_number
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
        plat_number = 'P16'
        item["plat_number"] = plat_number
        print('plat_number:',plat_number)

        author = ''.join(response.xpath('//*[@itemprop="author"]/text()').extract()).strip()
        print('author:',author)
        item["author"] = author
        novel_type = ''.join(response.xpath('//*[@itemprop="genre"]/text()').extract()).strip()
        if '-' in novel_type:
            novel_type = novel_type.replace('-',';')
        print('novel_type:',novel_type)
        item["novel_type"] = novel_type
        tags = response.xpath('//*[@class="smallreadbody"]/span/a/text() | //div[@class="smallreadbody"]/span[@style="color: red;"]//text()').extract()
        time.sleep(1)
        tags = ';'.join(tags)
        print('tags:',tags)
        item["tags"] = tags
        Signed = ''.join(response.xpath('//div[@class="righttd"]/ul[@class="rightul"]/li[last()-1]/b//text()').extract()).strip()
        if '已签约' in Signed:
            Signed = 1
        else:
            Signed = 0
        item["Signed"] = Signed
        print('Signed:', Signed)
        novel_desc = ''.join(response.xpath('//div[@id="novelintro"]//text()').extract()).strip()
        print('novel_desc:',novel_desc)
        item["novel_desc"] = novel_desc
        Product_image = plat_number + product_number
        Product_image = hashlib.md5(Product_image.encode(encoding='UTF-8')).hexdigest()
        print('Product_image:', Product_image)
        item["Product_image"] = Product_image
        P_image =  ''.join(response.xpath('//img[@itemprop="image"]/@src').extract()).strip()
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
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:',src_url)
        yield item