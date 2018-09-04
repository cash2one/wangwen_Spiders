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
    name = 'chuangshi_qq'
    allowed_domains = ['chuangshi.qq.com']
    start_urls = []
    lists = [
        'http://chuangshi.qq.com/bk/xh/349652.html?sword=焚天之怒',
        'http://chuangshi.qq.com/bk/ds/161342.html?sword=校花之贴身高手',
        'http://chuangshi.qq.com/bk/ds/19915605.html?sword=奶爸的文艺人生',
        'http://chuangshi.qq.com/bk/yx/216351.html?sword=联盟之谁与争锋',
        'http://chuangshi.qq.com/bk/xh/433109.html?sword=战神无敌',
        'http://chuangshi.qq.com/bk/xx/465030.html?sword=凡人修仙传',
        'http://chuangshi.qq.com/bk/yx/478670.html?sword=全职高手',
        'http://chuangshi.qq.com/bk/xx/475863.html?sword=遮天',
        'http://chuangshi.qq.com/bk/kh/503075.html?sword=异常生物见闻录',
        'http://chuangshi.qq.com/bk/ls/14175804.html?sword=逍遥小书生',
        'http://chuangshi.qq.com/bk/ds/832298.html?sword=重生之财源滚滚',
        'http://chuangshi.qq.com/bk/js/295037.html',
        'http://chuangshi.qq.com/bk/xh/481126.html?sword=武动乾坤',
        'http://chuangshi.qq.com/bk/xx/462522.html?sword=莽荒纪',
        'http://chuangshi.qq.com/bk/xh/462521.html?sword=完美世界',
        'http://chuangshi.qq.com/bk/xh/462523.html?sword=大主宰',
        'http://chuangshi.qq.com/bk/xh/15238666.html?sword=万界天尊',
        'http://chuangshi.qq.com/bk/ls/488347.html?sword=唐砖',
        'http://chuangshi.qq.com/bk/qc/215913.html?sword=余罪',
        'http://chuangshi.qq.com/bk/xh/462952.html?sword=将夜',
        'http://chuangshi.qq.com/bk/xx/485272.html?sword=最强弃少',
        'http://chuangshi.qq.com/bk/yx/222407.html?sword=穿越火线之AK传奇',
        'http://chuangshi.qq.com/bk/xh/14179514.html?sword=天道图书馆',
        'http://chuangshi.qq.com/bk/ds/479232.html?sword=校花的贴身高手',
        'http://chuangshi.qq.com/bk/xh/14608738.html?sword=圣墟',
        'http://chuangshi.qq.com/bk/ls/480068.html?sword=赘婿',
        'http://chuangshi.qq.com/bk/xx/819435.html?sword=一念永恒',
        'http://chuangshi.qq.com/bk/ds/20191960.html?sword=大王饶命',
        'http://chuangshi.qq.com/bk/xx/20468795.html?sword=飞剑问道',
        'http://chuangshi.qq.com/bk/ds/789906.html?sword=修真聊天群',
        'http://chuangshi.qq.com/bk/xx/20734492.html?sword=凡人修仙之仙界篇',
        'http://chuangshi.qq.com/bk/xh/19704712.html?sword=牧神记',
        'http://chuangshi.qq.com/bk/xh/804453.html?sword=斗罗大陆III龙王传说',
        'http://chuangshi.qq.com/bk/ls/20136878.html?sword=汉乡',
        'http://chuangshi.qq.com/bk/xh/462597.html?sword=帝霸',
        'http://chuangshi.qq.com/bk/xh/489745.html?sword=武炼巅峰',
        'http://chuangshi.qq.com/bk/ls/14185492.html?sword=带着仓库到大明',
        'http://chuangshi.qq.com/bk/ds/13541158.html?sword=我的1979',
        'http://chuangshi.qq.com/bk/xx/484840.html?sword=大道争锋',
        'http://chuangshi.qq.com/bk/xh/20399782.html?sword=太初',
        'http://chuangshi.qq.com/bk/xh/20868264.html?sword=诡秘之主',
        'http://chuangshi.qq.com/bk/qh/817386.html?sword=放开那个女巫',
        'http://chuangshi.qq.com/bk/ds/305138.html',
        'http://chuangshi.qq.com/bk/xh/263991.html',
        'http://chuangshi.qq.com/bk/ds/356087.html',
        'http://chuangshi.qq.com/bk/xh/353221.html',
        'http://chuangshi.qq.com/bk/ds/499686.html',
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
