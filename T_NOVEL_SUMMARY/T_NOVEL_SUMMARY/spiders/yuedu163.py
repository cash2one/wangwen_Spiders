# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,parse_time,chinese_to_arabic, parse_date
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

class Yuedu163Spider(scrapy.Spider):
    name = 'yuedu163'
    allowed_domains = ['yuedu.163.com']
    start_urls = []
    lists = [
        'http://yuedu.163.com/source/a798a334c1cd4445beeba9fc262a9735_4',
        'http://guofeng.yuedu.163.com/source/b3558290e6514e209511d5a3463b20bc_4'
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=======================',response.url)
        # print(response.text)
        item = TNovelSummaryItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h3[@title]/em/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P34'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update = ''.join(response.xpath('//div[@class="contents"]/div[@class="tab-item crt"]/a[@class="m-newupdate"]/h4/text()').extract()).strip()
        Chapter_num_update = ''.join(re.findall(r'第(.*?)章', Chapter_num_update, re.I|re.S))
        Chapter_num_update = chinese_to_arabic(Chapter_num_update)
        item["Chapter_num_update"] = Chapter_num_update
        print('Chapter_num_update:',Chapter_num_update)
        update_date = ''.join(response.xpath('//div[@class="contents"]/div[@class="tab-item crt"]/span[@class="updatetime"]/text()').extract()).replace('更新时间：','').strip()
        print('update_date:', update_date)
        update_date = parse_date(update_date)
        item["update_date"] = update_date
        print('update_date:',update_date)
        words = ''.join(response.xpath('//div[@class="m-bookstatus"]/table/tr//text()').extract()).strip()
        words = ''.join(re.findall(r'字数：(.*?)\n', words, re.I|re.M))
        words = process_number(words)
        item["words"] = words
        print('words:',words)
        click_num = ''.join(response.xpath('//div[@class="m-bookstatus"]/table/tr//text()').extract()).strip()
        click_num = ''.join(re.findall(r'点击：(.*?)\n', click_num, re.I|re.M))
        print('click_num:', click_num)
        click_num = process_number(click_num)
        item["click_num"] = click_num
        print('click_num:', click_num)
        score = ''.join(response.xpath('//div[@class="starlevel"]/span[@class="score"]/text()').extract()).strip()
        item["score"] = score
        print('score:',score)
        collect_num = None
        item["collect_num"] = collect_num
        bookid = ''.join(re.findall(r'source\/(.*)',src_url, re.I|re.M))
        link = 'http://yuedu.163.com/snsComment.do?operation=get&type=2&id={}'.format(bookid)
        # print(link)
        yield scrapy.Request(url=link, callback=self.parse_page_comment_num, meta={'item': item, 'bookid': bookid}, dont_filter=True)

    def parse_page_comment_num(self, response):
        print('2,==============================',response.url)
        item = response.meta["item"]
        text = response.text
        jsons = json.loads(text)
        # print(jsons)
        comment_num = jsons.get('totalCount')
        item["comment_num"] = comment_num
        print('comment_num:',comment_num)
        bookid = response.meta['bookid']
        link  = 'http://yuedu.163.com/presentRecord.do?operation=short&sourceUuid={}'.format(bookid)
        # print('link:',link)
        yield scrapy.Request(url=link, callback=self.parse_page_reward_num, meta={'item': item, 'bookid': bookid}, dont_filter=True)

    def parse_page_reward_num(self, response):
        print('3,=================================',response.url)
        item = response.meta["item"]
        bookid = response.meta['bookid']
        text = response.text
        jsons = json.loads(text)
        # print(jsons)
        reward_num = jsons.get('presentTotal')
        item["reward_num"] = reward_num
        print('reward_num:',reward_num)
        link = 'http://yuedu.163.com/monthlyTicketRecord.do?operation=short&sourceUuid={}'.format(bookid)
        yield scrapy.Request(url=link, callback=self.parse_page_tickets_num, meta={'item': item}, dont_filter=True)
    def parse_page_tickets_num(self, response):
        print('4,=======================',response.url)
        item = response.meta["item"]
        text = response.text
        jsons = json.loads(text)
        # print(jsons)
        tickets_num = jsons.get('thisMonthTotalVotes')
        item["tickets_num"] = tickets_num
        print('tickets_num:',tickets_num)
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)

        print(item)
        yield item