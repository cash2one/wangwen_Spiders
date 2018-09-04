# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
#from T_NOVEL.utils.process import process_date,process_number
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


class A17kSpider(scrapy.Spider):
    name = '17k'
    allowed_domains = ['www.17k.com']
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
        print('1,=======================',response.url)
        text = response.text
        item = TNovelSummaryItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//div[@class="Info Sign"]/h1/a[@target="_blank"]/text()').extract()).strip()
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P22'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update = None
        item["Chapter_num_update"] = Chapter_num_update
        print('Chapter_num_update:',Chapter_num_update)
        update_date_s = ''.join(response.xpath('//dl[@class="Tab"]/dt[@class="tit"]/em/text()').extract()).strip().replace('更新:','').strip()
        update_date = update_date_s + datetime.datetime.now().strftime(':%S')
        item["update_date"] = update_date
        print('update_date:',update_date)
        # timeArray = time.strptime(update_date_s, "%Y-%m-%d %H:%M")
        # timeStamp = int(time.mktime(timeArray))
        # print('timeStamp:', timeStamp)
        words = ''.join(response.xpath('//div[@class="BookData"]/p[last()-1]/em[@class="red"]/text()').extract()).strip()
        item["words"] = words
        print('words:',words)
        tickets_num = None
        item["tickets_num"] = tickets_num
        score = None
        item["score"] = score
        collect_num = None
        item["collect_num"] = collect_num
        reward_num = None
        item["reward_num"] = reward_num
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)

        authorId = re.findall(r'\/zuozhe\/(\d+)',text, re.I|re.M)[0]
        print('authorId:',authorId)
        bookId = ''.join(re.findall(r'([\d+]{4,6})',src_url, re.I|re.M))
        print('bookId:',bookId)
        click_num_link = 'http://api.ali.17k.com/v2/book/{}/stat_info?app_key=3362611833&click_info=1&hb_info=1&flower_info=1&stamp_info=1&cps_source='.format(bookId)
        yield scrapy.Request(url=click_num_link, callback=self.parse_page_click_num, meta={'item': item, 'bookId':bookId}, dont_filter=True)



    def parse_page_click_num(self, response):
        print('2,=========================',response.url)
        item = response.meta["item"]
        bookId = response.meta["bookId"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print(jsons)
        data = jsons.get('data')
        click_num = data.get('click_info').get('total_count')
        if click_num:
            item["click_num"] = click_num
            print('click_num:',click_num)
        else:
            click_num = 0
            item["click_num"] = click_num
            print('click_num:', click_num)

        comment_num_link = 'http://comment.17k.com/topic_list?bookId={}&commentType=all&order=1&page=1&pagesize=20'.format(bookId)
        yield scrapy.Request(url=comment_num_link, callback=self.parse_page_comment_num, meta={'item': item}, dont_filter=True)


    def parse_page_comment_num(self, response):
        print('3,======================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print(jsons)
        comment_num = jsons.get('page').get('count')
        item["comment_num"] = comment_num
        print('comment_num',comment_num)
        yield item
