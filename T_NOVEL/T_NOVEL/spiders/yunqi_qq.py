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

class QqSpider(scrapy.Spider):
    name = 'yunqi_qq'
    allowed_domains = ['yunqi.qq.com']
    start_urls = []
    lists = [
        'http://yunqi.qq.com/bk/xdyq/20304305.html',
        'http://yunqi.qq.com/bk/gdyq/19818084.html',
        'http://yunqi.qq.com/bk/xdyq/20427349.html?sword=后来偏偏喜欢你',
        'http://yunqi.qq.com/bk/xdyq/20624146.html?sword=余生漫漫皆为你',
        'http://yunqi.qq.com/bk/gdyq/185422.html?sword=一世倾城',
        'http://yunqi.qq.com/bk/gdyq/20540647.html?sword=重生最强女帝',
        'http://yunqi.qq.com/bk/xhyq/607991.html?sword=神医弃女',
        'http://yunqi.qq.com/bk/gdyq/11758803.html?sword=天医凤九',
        'http://yunqi.qq.com/bk/xdyq/14144781.html',
        'http://yunqi.qq.com/bk/xhyq/238544.html',
        'http://yunqi.qq.com/bk/xdyq/612464.html',
        'http://yunqi.qq.com/bk/xdyq/454426.html',
        'http://yunqi.qq.com/bk/xdyq/13648272.html?sword=许你万丈光芒好',
        'http://yunqi.qq.com/bk/gdyq/236549.html?sword=绝世神偷：废柴七小姐',
        'http://yunqi.qq.com/bk/xdyq/749834.html?sword=傲娇男神住我家',
        'http://yunqi.qq.com/bk/xdyq/243535.html?sword=拒嫁天王老公',
        'http://yunqi.qq.com/bk/xdyq/13700974.html?sword=那时喜欢你',
        'http://yunqi.qq.com/bk/gdyq/626275.html',
        'http://yunqi.qq.com/bk/xdyq/233707.html?sword=誓不为妻：全球豪娶少夫人',
        'http://yunqi.qq.com/bk/xhyq/317796.html?sword=纨绔仙医：邪帝毒爱妃',
        'http://yunqi.qq.com/bk/xdyq/16204776.html?sword=亿万星辰不及你',
        'http://yunqi.qq.com/bk/xdyq/234538.html?sword=他来了，请闭眼',
        'http://yunqi.qq.com/bk/xdyq/234538.html?sword=有123456',
        'http://yunqi.qq.com/bk/xdyq/234538.html?sword=如果蜗牛有爱情',
    ]
    for l in lists:
        start_urls.append(l)


    def parse(self, response):
        print('1,=====================',response.url)
        text = response.text
        # print(text)
        item = TNovelItem()
        url = response.url
        src_url = url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//img[@class="qqredaer_tit"]/@title').extract()).strip()
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P17'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        author =''.join(response.xpath('//*[@id="textauthor"]/following-sibling::p/a/text()').extract()).strip()
        item["author"] = author
        print('author:',author)
        novel_type = ';'.join(response.xpath('//div[@class="title"]/a[position()>1 and position()<last()]/text()').extract()).strip()
        item["novel_type"] = novel_type
        print('novel_type:',novel_type)
        tags = ''.join(response.xpath('//div[@class="tags"]/text()').extract()).strip().replace('作品标签：','')
        if tags:
            tags = tags.replace('、',';').strip()
        else:
            tags = ''
        item["tags"] = tags
        print('tags:',tags)
        Signed = ''.join(response.xpath('//div[@class="tag"]/div[@class="y"]/a[@title]/text()').extract()).strip()
        if '签约作品' in Signed:
            Signed = 1
        else:
            Signed = 0
        item["Signed"] = Signed
        print('Signed:',Signed)
        novel_desc = ''.join(response.xpath('//div[@class="info"]//text()').extract()).strip()
        item["novel_desc"] = novel_desc
        print('novel_desc:',novel_desc)
        Product_image = plat_number + product_number
        Product_image = hashlib.md5(Product_image.encode(encoding='UTF-8')).hexdigest()
        print('Product_image:', Product_image)
        item["Product_image"] = Product_image
        P_image = 'http:' + ''.join(response.xpath('//div[@class="cover"]/a[@class="bookcover"]/img/@src').extract()).strip()
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
