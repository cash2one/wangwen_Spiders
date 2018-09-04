# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_COMMENTS_PUB.items import TCommentsPubItem
from T_COMMENTS_PUB.utils.get_product_number import get_product_number
#from T_NOVEL.utils.process import process_date,process_number
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

class A3gscSpider(scrapy.Spider):
    name = '3gsc'
    allowed_domains = ['www.3gsc.com.cn']
    start_urls = []
    lists = [
        'http://www.3gsc.com.cn/book/235614',
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=======================',response.url)
        url = response.url
        item = TCommentsPubItem()
        src_url = url
        item["src_url"] = src_url
        print('src_url:', src_url)
        bookId = ''.join(re.findall(r'book\/(\d+)', url, re.I|re.M))
        print('bookId:',bookId)
        link = 'http://www.3gsc.com.cn/book/comment/{}'.format(bookId)
        yield scrapy.Request(url=link, callback=self.parse_page_link, meta={'item': item, 'bookId': bookId}, dont_filter=True)

    def parse_page_link(self, response):
        print('2,===========================',response.url)
        item = response.meta["item"]
        bookId = response.meta["bookId"]
        max_link = ''.join(response.xpath('//p[@class="page"]/a[last()]/@href').extract()).strip()
        print('max_link:',max_link)
        max_page = ''.join(re.findall(r'pn\/(\d+)',max_link, re.I|re.M))
        print('max_page:',max_page)
        for page in range(1, int(max_page)+1):
            link = 'http://www.3gsc.com.cn/book/comment/{}/new/pn/{}'.format(bookId,page)
            yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item}, dont_filter=True)

    def parse_page(self, response):
        print('3,================',response.url)
        item = response.meta["item"]
        uuid = response.xpath('//div[@uuid and @ class="box_synopsis"]/@uuid').extract()
        for id in uuid:
            print('id:',id)
            nick_name = ''.join(response.xpath('//div[@uuid = "{}"]/div[@class="cont"]/p[@class="nick_p"]/a/text()'.format(id)).extract()).strip()
            print('nick_name:',nick_name)
            item["nick_name"] = nick_name
            cmt_date = ''.join(response.xpath('//div[@uuid = "{}"]/div[@class="other"]/div[@class="data"]/i/text()'.format(id)).extract()).strip()
            item["cmt_date"] = cmt_date
            print('cmt_date:',cmt_date)
            cmt_time = ''.join(response.xpath('//div[@uuid = "{}"]/div[@class="other"]/div[@class="data"]/i/text()'.format(id)).extract()).strip()
            item["cmt_time"] = cmt_time
            print('cmt_time:',cmt_time)
            comments = ''.join(response.xpath('//div[@uuid = "{}"]/div[@class="cont"]/p[last()]//text()'.format(id)).extract()).strip()
            item["comments"] = comments
            print('comments:',comments)
            like_cnt = None
            item["like_cnt"] = like_cnt
            cmt_reply_cnt = ''.join(response.xpath('//div[@uuid = "{}"]/div[@class="other"]/div[@class="opt"]/span[last()]/text()'.format(id)).extract()).strip()
            item["cmt_reply_cnt"] = cmt_reply_cnt
            print('cmt_reply_cnt:',cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            product_number = ''.join(response.xpath('//div[@class="mod_name"]/p/a[@class="RecArticle"]/text()').extract()).strip()
            print('product_number:', product_number)
            # product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
            plat_number = 'P30'
            print('plat_number:', plat_number)
            item["plat_number"] = plat_number
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            print('last_modify_date:', last_modify_date)
            yield item



