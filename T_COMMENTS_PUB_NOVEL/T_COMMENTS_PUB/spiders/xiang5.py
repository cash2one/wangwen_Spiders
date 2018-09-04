# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_COMMENTS_PUB.items import TCommentsPubItem
from T_COMMENTS_PUB.utils.get_product_number import get_product_number
from T_COMMENTS_PUB.utils.process import process_date,process_number,parse_date
from scrapy_splash import SplashRequest, SplashFormRequest
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


class Xiang5Spider(scrapy.Spider):
    name = 'xiang5'
    allowed_domains = ['www.xiang5.com']
    start_urls = []
    lists = [
        'http://www.xiang5.com/bookinfo/24314.html'
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,==========================', response.url)
        if response.status != 200:
            yield scrapy.Request(url=response.url, callback=self.parse, dont_filter=True)
        else:
            print('请求成功>>>')
            item = TCommentsPubItem()
            src_url = response.url
            item["src_url"] = src_url
            print('src_url:', src_url)
            product_number = ' '.join(response.xpath('//div[@class=" fr worksLR"]/h4/text()').extract()).strip()
            print('product_number:', product_number)
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
            plat_number = 'P35'
            print('plat_number:', plat_number)
            item["plat_number"] = plat_number
            bookId = ''.join(re.findall(r'bookid\=(\d+)', src_url, re.I|re.M))
            print('bookId:',bookId)
            formdata = {
                'type': '1',
                'bookid': bookId,
                'page': '1',
            }
            link = 'http://www.xiang5.com/comment.php?a=allchangping'
            yield scrapy.FormRequest(url=link, formdata=formdata, callback=self.parse_page_max, meta={'item': item, 'bookId': bookId}, dont_filter=True)
    def parse_page_max(self, response):
        print('2,=============================',response.url)
        item = response.meta["item"]
        bookId = response.meta["bookId"]
        text = response.text
        max_page = ''.join(response.xpath('//*[@id="page"]/p/text()').extract()).strip()
        max_page = ''.join(re.findall(r'(\d+) 页', max_page, re.I|re.M))
        print('max_page:',max_page)
        for page in range(1, int(max_page)+1):
            formdata = {
                'type': '1',
                'bookid': bookId,
                'page': str(page),
            }
            link = 'http://www.xiang5.com/comment.php?a=allchangping'
            yield scrapy.FormRequest(url=link, formdata=formdata, callback=self.parse_page, meta={'item': item}, dont_filter=True)
    def parse_page(self, response):
        print('3,========================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(text)
        sel = etree.HTML(text)
        # print(type(sel))
        uids = ' '.join(sel.xpath('//div[@class="messageList"]/div[@class="fr messageListR"]/div[@class="messageListP"][1]/@id')).strip()
        uids = re.findall(r'brief_(\d+)',uids , re.I|re.M)
        # print('uids:',uids)
        for uid in uids:
            # print(uid)
            nick_name = ''.join(sel.xpath('//div[@class="messageList"]/div[@class="fr messageListR"]/div[@id="brief_{}"]/preceding-sibling::div[@class="messageListT"]/span/b/a/text()'.format(uid))).strip()
            item["nick_name"] = nick_name
            # print('nick_name:',nick_name)
            cmt_date = ''.join(sel.xpath('//div[@class="messageList"]/div[@class="fr messageListR"]/div[@id="brief_{}"]/preceding-sibling::div[@class="messageListT"]/span[last()]/text()'.format(uid))).strip()
            item["cmt_date"] = cmt_date
            # print('cmt_date:',cmt_date)
            cmt_time = ''.join(sel.xpath('//div[@class="messageList"]/div[@class="fr messageListR"]/div[@id="brief_{}"]/preceding-sibling::div[@class="messageListT"]/span[last()]/text()'.format(uid))).strip()
            item["cmt_time"] = cmt_time
            # print('cmt_time:', cmt_time)
            comments = ''.join(sel.xpath('//div[@class="messageList"]/div[@class="fr messageListR"]/div[@id="brief_{}"]/span/text()'.format(uid))).strip()
            item["comments"] = comments
            # print('comments:',comments)
            like_cnt = ''.join(sel.xpath('//div[@class="messageList"]/div[@class="fr messageListR"]/div[@class="messageListH"]/a/span[@id="good_{}"]/text()'.format(uid))).strip()
            item["like_cnt"] = like_cnt
            # print('like_cnt:',like_cnt)
            cmt_reply_cnt = ''.join(sel.xpath('//div[@class="messageList"]/div[@class="fr messageListR"]/div[@class="messageListH"]/a/span[@id="low_{}"]/../following-sibling::a[@class="colR"]/text()'.format(uid))).strip()
            cmt_reply_cnt = ''.join(re.findall(r'(\d+)',cmt_reply_cnt, re.I|re.M))
            item["cmt_reply_cnt"] = cmt_reply_cnt
            # print('cmt_reply_cnt:',cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            # print('last_modify_date:', last_modify_date)
            print('==============================================================')
            print(item)
            print('==================================================================')
            yield item




