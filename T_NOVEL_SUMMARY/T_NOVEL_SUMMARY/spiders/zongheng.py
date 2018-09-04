# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,chinesedigits,parse_time
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
import socket

class ZonghengSpider(scrapy.Spider):
    name = 'zongheng'
    allowed_domains = ['http://book.zongheng.com']
    start_urls = []

    base_urls = ''
    lists = [
         'http://book.zongheng.com/book/603738.html',
        'http://book.zongheng.com/book/523438.html',
        'http://book.zongheng.com/book/555035.html',
        'http://book.zongheng.com/book/568097.html',
        'http://book.zongheng.com/book/632434.html',
        'http://book.zongheng.com/book/635570.html',
        'http://book.zongheng.com/book/43467.html',
        'http://book.zongheng.com/book/682920.html',
        'http://book.zongheng.com/book/685640.html',
        'http://book.zongheng.com/book/512263.html',
        'http://book.zongheng.com/book/309318.html',
        'http://book.zongheng.com/book/457529.html',
        'http://book.zongheng.com/book/594492.html',
        'http://book.zongheng.com/book/342974.html',
        'http://book.zongheng.com/book/730066.html',
        'http://book.zongheng.com/book/510426.html',
        'http://book.zongheng.com/book/411993.html',
        'http://book.zongheng.com/book/45669.html',
        'http://book.zongheng.com/book/665301.html',
        'http://book.zongheng.com/book/401153.html',
        'http://book.zongheng.com/book/408586.html',
        'http://book.zongheng.com/book/481225.html',
        'http://book.zongheng.com/book/472101.html',
        'http://book.zongheng.com/book/431658.html',
        'http://book.zongheng.com/book/390470.html',
        'http://book.zongheng.com/book/524571.html',
        'http://book.zongheng.com/book/158432.html',
        'http://book.zongheng.com/book/688697.html',
        'http://book.zongheng.com/book/512648.html',
        'http://book.zongheng.com/book/470711.html',
        'http://book.zongheng.com/book/458842.html',
        'http://book.zongheng.com/book/189169.html',
        'http://book.zongheng.com/book/490372.html',
        'http://book.zongheng.com/book/435710.html',
        'http://book.zongheng.com/book/672340.html',
        'http://book.zongheng.com/book/47364.html',
        'http://book.zongheng.com/book/431145.html',
        'http://book.zongheng.com/book/280744.html',
        'http://book.zongheng.com/book/390021.html',
        'http://book.zongheng.com/book/251393.html',
        'http://book.zongheng.com/book/175703.html',
        'http://book.zongheng.com/book/570946.html',
        'http://book.zongheng.com/book/290053.html',
        'http://book.zongheng.com/book/525936.html',
        'http://book.zongheng.com/book/311835.html',
        'http://book.zongheng.com/book/732001.html',
        'http://book.zongheng.com/book/591444.html',
        'http://book.zongheng.com/book/69507.html',
        'http://book.zongheng.com/book/390199.html',
        'http://book.zongheng.com/book/347511.html',
        'http://book.zongheng.com/book/468543.html',
        'http://book.zongheng.com/book/472776.html',
        'http://book.zongheng.com/book/296950.html',
        'http://book.zongheng.com/book/513438.html',
        'http://book.zongheng.com/book/205411.html',
        'http://book.zongheng.com/book/121112.html',
        'http://book.zongheng.com/book/639927.html',
        'http://book.zongheng.com/book/88463.html',
        'http://book.zongheng.com/book/56579.html',
        'http://book.zongheng.com/book/568980.html',
        'http://book.zongheng.com/book/612328.html',
        'http://book.zongheng.com/book/676518.html',
        'http://book.zongheng.com/book/262883.html',
        'http://book.zongheng.com/book/720864.html',
        'http://book.zongheng.com/book/708632.html',
        'http://book.zongheng.com/book/377897.html',
        'http://book.zongheng.com/book/352542.html',
        'http://book.zongheng.com/book/646519.html',
        'http://book.zongheng.com/book/572891.html',
        'http://book.zongheng.com/book/36788.html',
        'http://book.zongheng.com/book/65189.html',
        'http://book.zongheng.com/book/578824.html',
        'http://book.zongheng.com/book/205836.html',
        'http://book.zongheng.com/book/714691.html',
        'http://book.zongheng.com/book/156062.html',
        'http://book.zongheng.com/book/450702.html',
        'http://book.zongheng.com/book/362880.html',
        'http://book.zongheng.com/book/645062.html',
        'http://book.zongheng.com/book/384410.html',

    ]

    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=======================',response.url)
        text = response.text
        # print(text)
        item = TNovelSummaryItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//div[@class="main"]/div[@class="status fl"]/h1/a/text()').extract()).strip()
        if '【' and '】' in product_number:
            product_number = product_number.replace('【', '[').replace('】', ']')
            print('product_number:', product_number)
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
        else:
            product_number = product_number
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
        plat_number = 'P21'
        item["plat_number"] = plat_number
        print('plat_number:', plat_number)
        Chapter_num_update = ''.join(response.xpath('//div[@class="update box"]/div[@class="cont"]/a/text()').extract()).strip()
        if Chapter_num_update:
            Chapter_num_update = ''.join(re.findall(u'第(.*?)部',Chapter_num_update, re.I|re.M))
            Chapter_num_update = chinesedigits(Chapter_num_update)
            item["Chapter_num_update"] = Chapter_num_update
            print('Chapter_num_update:',Chapter_num_update)
        update_date = ''.join(response.xpath('//div[@class="update box"]/div[@class="uptime"]/text()').extract()).strip().split('\n')[0].replace('·','')
        update_date = parse_time(update_date)
        item["update_date"] = update_date
        print('update_date:',update_date)
        words = ''.join(response.xpath('//div[@class="main"]/div[@class="status fl"]/div[@class="booksub"]/span[@title]/text()').extract()).strip()
        item["words"] = words
        print('words:',words)
        click_num = ' '.join(response.xpath('//div[@class="vote_info"]/p//text()').extract()).strip()
        if click_num:
            click_num = ''.join(re.findall(r'总点击： (\d+)',click_num, re.I|re.M))
        else:
            click_num = None
        item["click_num"] = click_num
        print('click_num:',click_num)
        comment_num = '  '.join(response.xpath('//div[@class="vote_info"]/p//text()').extract()).strip()
        if comment_num:
            comment_num = ''.join(re.findall(r'评论数：  (\d+)', comment_num, re.I|re.M))
        else:
            comment_num = None
        item["comment_num"] = comment_num
        print('comment_num:',comment_num)
        score = None
        item["score"] = score
        collect_num = '  '.join(response.xpath('//div[@class="vote_info"]/p//text()').extract()).strip()

        if collect_num:
            collect_num = ''.join(re.findall(r'总收藏：  (\d+)',collect_num, re.I|re.M))
        else:
            collect_num = None
        item["collect_num"] = collect_num
        print('collect_num:', collect_num)
        reward_num = None
        item["reward_num"] = reward_num
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        bookId = ''.join(re.findall(r'bookId=\"(\d+)\"', text, re.I|re.M))
        print('bookId:',bookId)
        link = 'http://book.zongheng.com/book/async/info.htm'
        formdata = {
            "bookId": bookId
        }
        yield scrapy.FormRequest(
            url=link,
            formdata=formdata,
            callback=self.parse_page,
            meta={'item': item},
            dont_filter=True,
        )
    def parse_page(self, response):
        print('2,======================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print(jsons)
        tickets_num = jsons.get('monthTicket').get('rank').get('number')
        item["tickets_num"] = tickets_num
        print('tickets_num:',tickets_num)
        yield item