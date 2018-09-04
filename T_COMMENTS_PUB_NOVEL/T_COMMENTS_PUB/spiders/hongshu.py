# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_COMMENTS_PUB.items import TCommentsPubItem
from T_COMMENTS_PUB.utils.get_product_number import get_product_number
from T_COMMENTS_PUB.utils.process import process_date,process_number,parse_time
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
        print('1,=======================',response.url)
        url = response.url
        item = TCommentsPubItem()
        src_url = url
        item["src_url"] = src_url
        print('src_url:', src_url)
        bookId = ''.join(re.findall(r'book\/(\d+)\/',url, re.I|re.M))
        print('bookId:',bookId)
        link = 'http://www.hongshu.com/comment/{}/index.do'.format(bookId)
        yield scrapy.Request(url=link, callback=self.parse_page_link, meta={'item':item, 'bookId': bookId}, dont_filter=True)

    def parse_page_link(self, response):
        print('2,======================',response.url)
        item = response.meta["item"]
        bookId = response.meta["bookId"]
        max_page_link = ''.join(response.xpath('//div[@category="npageList"]/form[@name="npageform"]/a[last()]/@href').extract()).strip()
        print('max_page_link:',max_page_link)
        max_page = re.search(r'npage\=(\d+)&',max_page_link , re.I|re.M).group(1)
        print('max_page:',max_page)
        for page in range(1,int(max_page)+1):
            link = 'http://www.hongshu.com/comment/{}/index.do?npage={}&pagesign=1'.format(bookId, page)
            yield scrapy.Request(url=link, callback=self.parse_page, meta={'item':item}, dont_filter=True)

    def parse_page(self, response):
        print('3,=====================',response.url)
        # print(response.text)
        item = response.meta["item"]
        uids = response.xpath('//div[@class="commentscon"]/ul/li[@id]/@id').extract()
        # print('uuid:',uid)
        for uid in uids:
            # print('uid:',uid)
            product_number = ''.join(response.xpath('//h2[@class="yahei"]/text()').extract()).strip()
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
            plat_number = 'P32'
            print('plat_number:', plat_number)
            item["plat_number"] = plat_number
            nick_name = ''.join(response.xpath('//li[@id="{}"]/div/p[@class="author2"]/a[@title]/text()'.format(uid)).extract()).strip()
            item["nick_name"] = nick_name
            print('nick_name:', nick_name)
            cmt_date = ''.join(response.xpath('//li[@id="{}"]/div/div/span/text()'.format(uid)).extract()).strip()
            # print('cmt_date:', cmt_date)
            cmt_date = parse_time(cmt_date)
            item["cmt_date"] = cmt_date
            print('cmt_date:', cmt_date)
            cmt_time = ''.join(response.xpath('//li[@id="{}"]/div/div/span/text()'.format(uid)).extract()).strip()
            # print('cmt_date:', cmt_date)
            cmt_time = parse_time(cmt_time)
            item["cmt_time"] = cmt_time
            print('cmt_time', cmt_time)
            comments = ''.join(response.xpath('//li[@id="{}"]/div/a/p/text()'.format(uid)).extract()).strip()
            if comments:
                item["comments"] = comments
                print('comments:', comments)
            else:
                comments = ''.join(response.xpath('//li[@id="{}"]/div[@class="right rtdashang"]/a/div//text()'.format(uid)).extract()).strip()
                item["comments"] = comments
                print('comments:', comments)
            like_cnt = ''.join(response.xpath('//li[@id="{}"]/div/div/a[last()-1]/c/text()'.format(uid)).extract()).strip()
            # print('like_cnt:', like_cnt)
            if like_cnt:
                item["like_cnt"] = like_cnt
                print('like_cnt:', like_cnt)
            else:
                like_cnt = 0
                item["like_cnt"] = like_cnt
                print('like_cnt:', like_cnt)
            cmt_reply_cnt = ''.join(response.xpath('//li[@id="{}"]/div/div/a[last()]/text()'.format(uid)).extract()).strip().replace('回复(','').replace(')','')
            # print('cmt_reply_cnt:', cmt_reply_cnt)
            if cmt_reply_cnt:
                item["cmt_reply_cnt"] = cmt_reply_cnt
                print('cmt_reply_cnt:', cmt_reply_cnt)
            else:
                cmt_reply_cnt = 0
                item["cmt_reply_cnt"] = cmt_reply_cnt
                print('cmt_reply_cnt:', cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            print('last_modify_date:', last_modify_date)
            yield item
