# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,chinese_to_arabic,parse_time
from scrapy_splash import SplashRequest, SplashFormRequest
# from IqiyiSpider.getItem import get_item
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

class HeiyanSpider(scrapy.Spider):
    name = 'heiyan'
    allowed_domains = ['www.heiyan.com']
    start_urls = []
    lists = [
        'http://www.heiyan.com/book/25058'
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=========================',response.url)
        text = response.text
        # print(text)
        item = TNovelSummaryItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h2/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P31'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update = ''.join(response.xpath('//h4/a/text()').extract()).strip()
        Chapter_num_update = ''.join(re.findall(r'第([\u4e00-\u9fa5]{1,10})章', Chapter_num_update, re.I|re.M))
        Chapter_num_update = chinese_to_arabic(Chapter_num_update)
        item["Chapter_num_update"] = Chapter_num_update
        print('Chapter_num_update:',Chapter_num_update)
        update_date = ''.join(response.xpath('//h4/span[@class="time"]/text()').extract()).strip()
        update_date = parse_time(update_date)
        item["update_date"] = update_date
        print('update_date:',update_date)
        words = ''.join(response.xpath('//span[@class="words"]/text()').extract()).strip()
        words = ''.join(re.findall(r'(\d+)字',words, re.I|re.M))
        item["words"] = words
        print('words:',words)
        tickets_num = None
        item["tickets_num"] = tickets_num
        score = None
        item["score"] = score
        reward_num = None
        item["reward_num"] = reward_num
        bookId = ''.join(re.findall(r'book\/(\d+)', src_url, re.I|re.M))
        link = 'http://a.heiyan.com/ajax/book/extend/{}/detail'.format(bookId)
        # print('link:',link)
        yield scrapy.Request(url=link, callback=self.parse_page_click_num, meta={'item': item, 'bookId': bookId}, dont_filter=True)
    def parse_page_click_num(self, response):
        print('2,=============================',response.url)
        item = response.meta["item"]
        text = response.text
        jsons = json.loads(text)
        # print(jsons)
        click_num = jsons.get('readPV')
        # click_num = ''.join(re.findall(r'(\d+)点击', click_num, re.I|re.M))
        item["click_num"] = click_num
        print('click_num:', click_num)
        collect_num = jsons.get('FOLLOWER_COUNT')
        item["collect_num"] = collect_num
        print('collect_num:',collect_num)
        bookId = response.meta["bookId"]
        link  = 'http://review.heiyan.com/jsonp/review/{}'.format(bookId)
        yield scrapy.Request(url=link, callback=self.parse_page_comment_num, meta={'item': item, 'bookId': bookId},dont_filter=True)

    def parse_page_comment_num(self, response):
        print('3,============================',response.url)
        item = response.meta["item"]
        text = response.text
        jsons = json.loads(text)
        # print(jsons)
        comment_num = jsons.get('reviewCount')
        item["comment_num"] = comment_num
        print('comment_num:',comment_num)
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        print(item)
        yield item




