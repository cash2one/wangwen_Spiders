# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number
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


class A3gscSpider(scrapy.Spider):
    name = '3gsc'
    allowed_domains = ['http://www.3gsc.com.cn']
    start_urls = []
    lists = [
        'http://www.3gsc.com.cn/book/235614'
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
        product_number = ''.join(response.xpath('//h1[@class="RecArticle"]//text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P30'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update = ''.join(response.xpath('//*[@id="con_ListStyleBTab2C_1"]/div[@class="area"]/span/a/b/text()').extract()).strip()
        Chapter_num_update = ''.join(re.findall(r'(\d+)', Chapter_num_update, re.I|re.M))
        item["Chapter_num_update"] = Chapter_num_update
        print('Chapter_num_update:',Chapter_num_update)
        update_date = ''.join(response.xpath('//*[@id="con_ListStyleBTab2C_1"]/div[@class="area"]/span/text()').extract()).strip()
        update_date = ''.join(re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', update_date, re.I|re.M))
        item["update_date"] = update_date
        print('update_date:',update_date)
        tickets_num = ''.join(response.xpath('//div[@class="inter_con"]/div[@class="give"]/ul/li[@id="Interbt3"]/p/span/text()').extract()).strip()
        item["tickets_num"] = tickets_num
        print('tickets_num:',tickets_num)
        reward_num = ''.join(response.xpath('//div[@class="inter_con"]/div[@class="give"]/ul/li[@id="Interbt1"]/p/span/text()').extract()).strip()
        item["reward_num"] = reward_num
        print('reward_num:',reward_num)
        score = None
        item["score"] = score
        book_id = ''.join(re.findall(r'book\/(\d+)', src_url, re.I|re.M))
        print('book_id:',book_id)
        link = 'http://www.3gsc.com.cn/BookLazyload/getstatis?book_id={}'.format(book_id)
        yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item, 'book_id':book_id}, dont_filter=True)

        comment_num_link = ''.join(response.xpath('//div[@class="forum_stati"]/div[@class="opt"]/a/@href').extract()).strip()
        if comment_num_link:
            comment_num_link = 'http://www.3gsc.com.cn' + comment_num_link
            yield scrapy.Request(url=comment_num_link, callback=self.parse_page_comment_num, meta={'item': item}, dont_filter=True)
        else:
            print('没找到连接////')

    def parse_page(self, response):
        print('2,=========================',response.url)
        item = response.meta["item"]
        text = response.text
        jsons = json.loads(text)
        # print(jsons)
        data = jsons.get('data')
        # print(data)
        words = data.get('word_count')
        words = process_number(words)
        item["words"] = words
        print('words:',words)
        click_num = data.get('day_hit_total')
        item["click_num"] = click_num
        print('click_num:',click_num)
        collect_num = data.get('day_recom_total')
        item["collect_num"] = collect_num
        print('collect_num:',collect_num)


    def parse_page_comment_num(self, response):
        print('3,==============================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(text)
        comment_num = ''.join(response.xpath('//*[@class = "page"]/text()').extract()).strip()
        comment_num = ''.join(re.findall(r'(\d+) 条记录', comment_num, re.I|re.M))
        item["comment_num"] = comment_num
        print('comment_num:',comment_num)
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)

        print(item)
        yield item


