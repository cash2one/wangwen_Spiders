# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL.items import TNovelItem
from T_NOVEL.utils.get_product_number import get_product_number
from T_NOVEL.utils.process import process_date,process_number
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

class Xiang5Spider(scrapy.Spider):
    name = 'xiang5'
    allowed_domains = ['www.xiang5.com']
    start_urls = []
    lists = [
        'http://www.xiang5.com/bookinfo/24314.html'
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=========================',response.url)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "UM_distinctid=164daf563af44a-0b77993c46f21-6114147a-100200-164daf563b0422; canal=0; schannelm=0; www_say=775abff326250295f011c827045e4f45; PHPSESSID=imbduief49qgu8e9mttjtb03u1; Hm_lvt_688746b9e4f9d33e0e2ce6aeffb4fa58=1535520731,1535597551; counter=zixing; countertime=2018/8/30; _jzqc=1; _qzjc=1; CNZZDATA1253179669=891460335-1532681545-%7C1535606694; Hm_lpvt_688746b9e4f9d33e0e2ce6aeffb4fa58=1535610428; uuid=2AE001D147E7F1C7E3026160C9234536; marks=13; _qzja=1.754836888.1532681874609.1535597551629.1535610427783.1535602634139.1535610427783.0.0.0.22.6; _qzjto=18.2.0; _jzqa=1.4298357099084273000.1532681875.1535597552.1535610428.6; _jzqx=1.1535610428.1535610428.1.jzqsr=xiang5%2Ecom|jzqct=/.-; _jzqckmp=1; _jzqb=1.1.10.1535610428.1; _qzjb=1.1535610427783.1.0.0.0",
            "Host": "www.xiang5.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }
        if response.status != 200:
            yield scrapy.Request(url=response.url, headers=headers, callback=self.parse, dont_filter=True)
        else:
            print('请求成功>>>')
            item = TNovelItem()
            src_url = response.url
            item["src_url"] = src_url
            print('src_url:', src_url)
            product_number = ' '.join(response.xpath('//div[@class=" fr worksLR"]/h4/text()').extract()).strip()
            print('product_number:', product_number)
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
            plat_number = 'P35'
            print('plat_number:', plat_number)
            item["plat_number"] = plat_number
            author = ''.join(response.xpath('//div[@class="workSecTitle"]/span/b[@class=" colR"]/a/text()').extract()).strip()
            item["author"] = author
            print('author:', author)
            novel_type = ';'.join(response.xpath('//div[@class="pos"]/a[2]/text()').extract()).strip()
            item["novel_type"] = novel_type
            print('novel_type:', novel_type)
            tags = ';'.join(response.xpath('//div[@class="workInfoList"]/span/b[@class="colR"]/a/text()').extract()).strip()
            item["tags"] = tags
            print('tags:',tags)
            Signed_s = ''.join(response.xpath('//div[@class="workInfoList"]/span/b[@class="colR"]/text()').extract()).strip()
            if '签约' in Signed_s:
                Signed = 1
            else:
                Signed = 0
            item["Signed"] = Signed
            print('Signed:', Signed)
            novel_desc = ''.join(response.xpath('//div[@class=" fr worksLR"]/p[@style]/text()').extract()).strip()
            item["novel_desc"] = novel_desc
            print('novel_desc:', novel_desc)
            Product_image = plat_number + product_number
            Product_image = hashlib.md5(Product_image.encode(encoding='UTF-8')).hexdigest()
            print('Product_image:', Product_image)
            item["Product_image"] = Product_image
            P_image = 'http:' + ''.join(response.xpath('//*[@id="sendprize"]/div[@class="fl worksLL"]/a[@title]/img/@src').extract()).strip()
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


