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
import math

class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['book.qidian.com']

    def start_requests(self):
        base_urls = [
            'https://book.qidian.com/info/3347812',
            'https://book.qidian.com/info/3394903',
            'https://book.qidian.com/info/1009915605',
            'https://book.qidian.com/info/3347395',
            'https://book.qidian.com/info/3363928',
            'https://book.qidian.com/info/107580',
            'https://book.qidian.com/info/1887208',
            'https://book.qidian.com/info/1735921',
            'https://book.qidian.com/info/3242304',
            'https://book.qidian.com/info/1004175804',
            'https://book.qidian.com/info/1003580078',
            'https://book.qidian.com/info/3348326',
            'https://book.qidian.com/info/2048120',
            'https://book.qidian.com/info/2502372',
            'https://book.qidian.com/info/2952453',
            'https://book.qidian.com/info/2750457',
            'https://book.qidian.com/info/1005238666',
            'https://book.qidian.com/info/2413595',
            'https://book.qidian.com/info/3348312',
            'https://book.qidian.com/info/2083259',
            'https://book.qidian.com/info/2248950',
            'https://book.qidian.com/info/3358605',
            'https://book.qidian.com/info/1004179514',
            'https://book.qidian.com/info/1001579096',
            'https://book.qidian.com/info/1931432',
            'https://book.qidian.com/info/1004608738',
            'https://book.qidian.com/info/1979049',
            'https://book.qidian.com/info/1003354631',
            'https://book.qidian.com/info/1010191960',
            'https://book.qidian.com/info/1010468795#Catalog',
            'https://book.qidian.com/info/3602691',
            'https://book.qidian.com/info/1010734492',
            'https://book.qidian.com/info/1009704712',
            'https://book.qidian.com/info/3681560',
            'https://book.qidian.com/info/1010136878',
            'https://book.qidian.com/info/3258971',
            'https://book.qidian.com/info/2494758',
            'https://book.qidian.com/info/1004185492',
            'https://book.qidian.com/info/1003541158',
            'https://book.qidian.com/info/2226569',
            'https://book.qidian.com/info/1010399782',
            'https://book.qidian.com/info/1010868264',
            'https://book.qidian.com/info/1003306811',
        ]
        for url in base_urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse_page,
                dont_filter=True,
            )
    def parse_page(self, response):
        print('1,=====================',response.url)
        # print(response.text)
        item = TCommentsPubItem()
        src_url = response.url
        item["src_url"] = src_url
        bookId = src_url.replace('https://book.qidian.com/info/','')
        print('bookId:',bookId)
        link = 'https://book.qidian.com/ajax/book/GetBookForum?_csrfToken=HUc4mzWMTveOYkK01P9mREV04r5f0zisvnDNZl7j&authorId=0&bookId={}&chanId=0&pageSize=15'.format(bookId)
        yield scrapy.Request(url=link, callback=self.parse_page_link, meta={'item': item}, dont_filter=True)
    def parse_page_link(self,response):
        print('2,=====================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(response.text)
        jsons = json.loads(text)
        forumId = jsons.get('data').get('forumId')
        print('forumId:',forumId)
        link = 'https://forum.qidian.com/index/{}?type=1&page=1'.format(forumId)
        yield scrapy.Request(url=link, callback=self.parse_page_p, meta={'item': item, 'forumId': forumId}, dont_filter=True)
    def parse_page_p(self, response):
        print('3,=======================',response.url)
        item = response.meta["item"]
        forumId = response.meta["forumId"]
        # print(response.text)
        pagemax = ''.join(response.xpath('//div[@data-pagemax]/@data-pagemax').extract()).strip()
        print('pagemax:',pagemax)
        for page in range(1,int(pagemax)+1):
            # print(page)
            url = 'https://forum.qidian.com/index/{}?type=1&page={}'.format(forumId,str(page))
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_new_page, meta={'item': item},dont_filter=True)
    def parse_new_page(self, response):
        print('4,==========================',response.url)
        # print(response.text)
        uids = response.xpath('//div[@data-g]/@data-g').extract()
        for uid in uids:
            # print(uid)
            time.sleep(1)
            item = response.meta["item"]
            product_number = ''.join(response.xpath('//h1/a/text()').extract()).strip()
            product_number = get_product_number(product_number)
            # print('product_number:', product_number)
            item["product_number"] = product_number
            plat_number = 'P20'
            # print('plat_number:', plat_number)
            item["plat_number"] = plat_number
            long_comment = 0
            item["long_comment"] = long_comment
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            # print('last_modify_date:', last_modify_date)
            nick_name_s = response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-auther"]/a/text()'.format(uid)).extract()
            if len(nick_name_s) > 1:
                for ni in nick_name_s:
                    time.sleep(1)
                    nick_name = ni.strip()
                    item["nick_name"] = nick_name
                    # print('nick_name:', nick_name)
                    cmt_date_s = response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-info dib-wrap"]/span/text()'.format(uid)).extract()
                    for cd in cmt_date_s:
                        time.sleep(1)
                        cmt_date = cd.strip().replace('更新','')
                        # print('cmt_date:', cmt_date)
                        cmt_date = parse_time(cmt_date)
                        item["cmt_date"] = cmt_date
                        # print('cmt_date:', cmt_date)
                        cmt_time_s = response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-info dib-wrap"]/span/text()'.format(uid)).extract()
                        for ct in cmt_time_s:
                            time.sleep(1)
                            cmt_time = ct.strip().replace('更新','')
                            cmt_time = parse_time(cmt_time)
                            item["cmt_time"] = cmt_time
                            # print('cmt_time:', cmt_time)
                            comments_s = response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-body"]/a/text()'.format(uid)).extract()
                            for cm in comments_s:
                                time.sleep(1)
                                comments = cm.strip()
                                item["comments"] = comments
                                # print('comments:', comments)
                                like_cnt_s = response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-info dib-wrap"]/a[@class="info-tab like-btn"]/span/text()'.format(uid)).extract()
                                for lk in like_cnt_s:
                                    time.sleep(1)
                                    like_cnt = lk.strip().replace('赞','')
                                    item["like_cnt"] = like_cnt
                                    # print('like_cnt:',like_cnt)
                                    cmt_reply_cnt_s = response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-info dib-wrap"]/a[@class="info-tab mr20"]/span/text()'.format(uid)).extract()
                                    for cr in cmt_reply_cnt_s:
                                        time.sleep(1)
                                        cmt_reply_cnt = cr.strip().replace('条回复','')
                                        item["cmt_reply_cnt"] = cmt_reply_cnt
                                        # print('cmt_reply_cnt:', cmt_reply_cnt)
                                        print(item)
                                        # yield item
            else:
                nick_name = ''.join(response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-auther"]/a/text()'.format(uid)).extract()).strip()
                item["nick_name"] = nick_name
                # print('nick_name:',nick_name)
                cmt_date = ''.join(response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-info dib-wrap"]/span/text()'.format(uid)).extract()).strip().replace('更新','')
                # print('cmt_date:', cmt_date)
                cmt_date = parse_time(cmt_date)
                item["cmt_date"] = cmt_date
                # print('cmt_date:',cmt_date)
                cmt_time = ''.join(response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-info dib-wrap"]/span/text()'.format(uid)).extract()).strip().replace('更新','')
                cmt_time = parse_time(cmt_time)
                item["cmt_time"] = cmt_time
                # print('cmt_time:',cmt_time)
                comments = ''.join(response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-body"]/a/text()'.format(uid)).extract()).strip()
                item["comments"] = comments
                # print('comments:',comments)
                like_cnt = ''.join(response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-info dib-wrap"]/a[@class="info-tab like-btn"]/span/text()'.format(uid)).extract()).strip().replace('赞','')
                item["like_cnt"] = like_cnt
                # print('like_cnt:',like_cnt)
                cmt_reply_cnt = ''.join(response.xpath('//div[@data-g="{}"]/following-sibling::div[@class="post"]/p[@class="post-info dib-wrap"]/a[@class="info-tab mr20"]/span/text()'.format(uid)).extract()).strip().replace('条回复','')
                item["cmt_reply_cnt"] = cmt_reply_cnt
                # print('cmt_reply_cnt:',cmt_reply_cnt)
                print('item:',item)

            yield item