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
import socket


class JjwxcSpider(scrapy.Spider):
    name = 'jjwxc'
    allowed_domains = ['http://www.jjwxc.net']
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
        item = TNovelSummaryItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h1[@itemprop="name"]/span/text()').extract()).strip()
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
        plat_number = 'P16'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update = ''.join(response.xpath('//*[@id="oneboolt"]/tbody/tr[last()-1]/td[1]//text()').extract()).strip()
        print('Chapter_num_update:',Chapter_num_update)
        item["Chapter_num_update"] = Chapter_num_update
        update_date = ''.join(response.xpath('//*[@id="oneboolt"]/tbody/tr[last()-1]/td[last()]/span[1]/text()').extract()).strip()
        print('update_date:',update_date)
        item["update_date"] = update_date
        words = ''.join(response.xpath('//*[@class="righttd"]/ul[@class="rightul"]/li/span[@itemprop="wordCount"]/text()').extract()).strip().replace('字','')
        print('words:',words)
        item["words"] = words
        tickets_num = None
        item["tickets_num"] = tickets_num
        comment_num = ''.join(response.xpath('//*[@id="oneboolt"]/tbody/tr[last()]/td/div/span[@itemprop="reviewCount"]/text()').extract())
        print('comment_num:',comment_num)
        item["comment_num"] = comment_num
        score = None
        item['score'] = score
        collect_num = ''.join(response.xpath('//*[@id="oneboolt"]/tbody/tr[last()]/td/div/span[@itemprop="collectedCount"]//text()').extract()).strip()
        print('collect_num:',collect_num)
        item["collect_num"] = collect_num
        reward_num = None
        item["reward_num"] = reward_num
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        # driver = webdriver.PhantomJS(executable_path='D:\WGSruanjian\phantomjs-2.1.1-windows/bin/phantomjs.exe')
        # driver = webdriver.Chrome()
        # socket.setdefaulttimeout(20)
        # driver.get(src_url)
        # click_num = driver.find_element_by_xpath('//*[@id="totleclick"]').text
        # driver.close()
        # print('click_num:', click_num)
        # item["click_num"] = click_num

        yield SplashRequest(url=src_url, callback=self.parse_page, args={'wait': 0.5},meta={'item': item}, dont_filter=True)

    def parse_page(self, response):
        print('2,========================',response.url)
        item = response.meta['item']
        text = response.text
        # print(text)
        click_num = ''.join(response.xpath('//*[@id="totleclick"]/text()').extract()).strip()
        item["click_num"] = click_num
        print('click_num:',click_num)
        yield item