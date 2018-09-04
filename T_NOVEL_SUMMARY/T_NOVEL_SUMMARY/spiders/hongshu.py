# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,parse_time
from scrapy_splash import SplashRequest, SplashFormRequest
from scrapy_redis.spiders import RedisSpider
from selenium import webdriver
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
from locale import *
setlocale(LC_NUMERIC, 'English_US')


class HongshuSpider(scrapy.Spider):
    name = 'hongshu'
    allowed_domains = ['www.hongshu.com']
    start_urls = []
    lists = [
        'http://www.hongshu.com/book/56983/'
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,==========================',response.url)
        text = response.text
        # print(text)
        item = TNovelSummaryItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h1[@class="fllf"]/a[@title]/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P32'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update = ''.join(response.xpath('//h3[@class="bom10"]/a[@class="cboy"]/text()').extract()).strip()
        Chapter_num_update = ''.join(re.findall(r'第(\d+)章', Chapter_num_update ,re.I|re.M))
        item["Chapter_num_update"] = Chapter_num_update
        print('Chapter_num_update:',Chapter_num_update)
        update_date = ''.join(response.xpath('//h3[@class="bom10"]/span[@class="lf10"]/text()').extract()).strip()
        update_date = parse_time(update_date)
        item["update_date"] = update_date
        print('update_date:',update_date)
        words = ' '.join(response.xpath('//div[@class="right"]/p[@class="infor bom10"]/span/text()').extract()).strip()
        words = ''.join(re.findall(r'总字数：(.*?)\s', words, re.I|re.M))
        words = process_number(words)
        item["words"] = words
        print('words:',words)
        click_num = ' '.join(response.xpath('//div[@class="right"]/p[@class="infor bom10"]/span/text()').extract()).strip()
        click_num = ''.join(re.findall(r'点击：(.*?)\s ', click_num, re.I|re.M))
        print('click_num:',click_num)
        if '万' in click_num:
            click_num = click_num.replace('万','')
            click_num = int(atof(click_num)*10000)
            item["click_num"] = click_num
            print('click_num:', click_num)
        else:
            click_num = int(atof(click_num))
            item["click_num"] = click_num
            print('click_num:',click_num)
        tickets_num = None
        item["tickets_num"] = tickets_num
        comment_num = ''.join(response.xpath('//div[@category="comment"]/a[@class="tabfmbtn cboy"]/text()').extract()).strip()
        comment_num = ''.join(re.findall(r'最新书评(.*)', comment_num, re.I|re.S)).replace('(','').replace(')','')
        comment_num = int(atof(comment_num))
        item["comment_num"] = comment_num
        print('comment_num:',comment_num)
        score = None
        item["score"] = score
        collect_num = None
        item["collect_num"] = collect_num
        reward_num = None
        item["reward_num"] = reward_num
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)

        print(item)
        yield item
