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


class HeiyanSpider(scrapy.Spider):
    name = 'heiyan'
    allowed_domains = ['review.heiyan.com']
    start_urls = []
    lists = [
        'http://www.heiyan.com/book/25058'
    ]

    for l in lists:
        start_urls.append(l)
    def parse(self,response):
        print('1,=========================',response.url)
        url = response.url
        bookId = ''.join(re.findall(r'book\/(\d+)',url, re.I|re.M))
        print('bookId:',bookId)
        link = 'http://review.heiyan.com/book/{}/review'.format(bookId)
        yield scrapy.Request(url=link, callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        print('2,==================',response.url)
        # print(response.text)
        item = TCommentsPubItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        uids = response.xpath('//div[@class="mod comments reviews"]/div[@class="bd"]/ul/li[@data-feed-id]/@data-feed-id').extract()
        # print('uids:',uids)
        for uid in uids:
            print('uid:',uid)
            product_number = ''.join(response.xpath('//h1[@class="page-title"]/text() | //h2/text()').extract()).strip().replace('的评论','')
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
            plat_number = 'P31'
            print('plat_number:', plat_number)
            item["plat_number"] = plat_number
            nick_name = ''.join(response.xpath('//div[@class="mod comments reviews"]/div[@class="bd"]/ul/li[@data-feed-id="{}"]/div[@class="left"]/a[@class="name"]/text()'.format(uid)).extract()).strip()
            item["nick_name"] = nick_name
            print('nick_name:',nick_name)
            cmt_date = ''.join(response.xpath('//div[@class="mod comments reviews"]/div[@class="bd"]/ul/li[@data-feed-id="{}"]/div[@class="right"]/div[@class="controls"]/span[@class="time"]/text()'.format(uid)).extract()).strip()
            item["cmt_date"] = cmt_date
            print('cmt_date:',cmt_date)
            cmt_time = ''.join(response.xpath('//div[@class="mod comments reviews"]/div[@class="bd"]/ul/li[@data-feed-id="{}"]/div[@class="right"]/div[@class="controls"]/span[@class="time"]/text()'.format(uid)).extract()).strip()
            item["cmt_time"] = cmt_time
            print('cmt_time',cmt_time)
            comments = ''.join(response.xpath('//div[@class="mod comments reviews"]/div[@class="bd"]/ul/li[@data-feed-id="{}"]/div[@class="right"]/p[@class="summary"]//text()'.format(uid)).extract()).strip()
            if comments:
                item["comments"] = comments
                print('comments:',comments)
            else:
                comments = ''.join(response.xpath('//div[@class="mod comments reviews"]/div[@class="bd"]/ul/li[@data-feed-id="{}"]/div[@class="right"]/h3/a/text()'.format(uid)).extract()).strip()
                item["comments"] = comments
                print('comments:', comments)
            like_cnt = ''.join(response.xpath('//div[@class="mod comments reviews"]/div[@class="bd"]/ul/li[@data-feed-id="{}"]/div[@class="left"]/p/img/@title'.format(uid)).extract()).strip()
            if like_cnt:
                like_cnt = ''.join(re.findall(r'粉丝值：\d+',like_cnt)).replace('粉丝值：','')
                item["like_cnt"] = like_cnt
                print('like_cnt:', like_cnt)
            else:
                like_cnt = 0
                item["like_cnt"] = like_cnt
                print('like_cnt:',like_cnt)
            cmt_reply_cnt = ''.join(response.xpath('//div[@class="mod comments reviews"]/div[@class="bd"]/ul/li[@data-feed-id="{}"]/div[@class="right"]/div[@class="controls"]/a[@action-type="comment"]/span[@class="num"]/text()'.format(uid)).extract()).strip()
            if cmt_reply_cnt:
                item["cmt_reply_cnt"] = cmt_reply_cnt
                print('cmt_reply_cnt:',cmt_reply_cnt)
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

        next_page_url = ''.join(response.xpath('//div[@class="pagination"]/p/a[@class="btn next"]/@href').extract()).strip()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse_page, dont_filter=True)




