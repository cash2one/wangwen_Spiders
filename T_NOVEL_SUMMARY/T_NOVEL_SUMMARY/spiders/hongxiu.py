# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,parse_time
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

class HongxiuSpider(scrapy.Spider):
    name = 'hongxiu'
    allowed_domains = ['www.hongxiu.com']
    start_urls = [
        'https://www.hongxiu.com/book/8263527304935303'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse, args={'wait': 1})

    def parse(self, response):
        print('1,======================',response.url)
        text = response.text
        # print(text)
        item = TNovelSummaryItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h1/em/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P33'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update = ''.join(response.xpath('//div[@class="update"]/p/a/text()').extract()).strip()
        Chapter_num_update = ''.join(re.findall(r'第(\d+)章', Chapter_num_update, re.I|re.S))
        item["Chapter_num_update"] = Chapter_num_update
        print('Chapter_num_update:',Chapter_num_update)
        update_date = ''.join(response.xpath('//div[@class="update"]/p/span/text()').extract()).strip()
        update_date = parse_time(update_date)
        item["update_date"]  =update_date
        print('update_date:',update_date)
        words = ''.join(response.xpath('//div[@class="book-info"]/p[@class="total"]//text()').extract()).strip()
        words = ''.join(re.findall(r'(.*?)字\|', words, re.I|re.S))
        words = process_number(words)
        item["words"] = words
        print('words:',words)
        click_num = ''.join(response.xpath('//div[@class="book-info"]/p[@class="total"]//text()').extract()).strip()
        click_num = ''.join(re.findall(r'([0-9]+\.[0-9]+万)总点击', click_num))
        print('click_num:', click_num)
        click_num = process_number(click_num)
        item["click_num"] = click_num
        print('click_num:',click_num)
        tickets_num = ''.join(response.xpath('//*[@id="monthCount"]/text()').extract()).strip()
        item["tickets_num"] = tickets_num
        print('tickets_num:',tickets_num)
        comment_num = ''.join(response.xpath('//div[@class="lbf-pagination"]/ul/li[last()-1]/a/text()').extract()).strip()
        if comment_num:
            comment_num = int(comment_num)*10
        else:
            comment_num = 10
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

