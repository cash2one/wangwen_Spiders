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

class IreaderSpider(scrapy.Spider):
    name = 'ireader'
    allowed_domains = ['http://www.ireader.com']
    start_urls = []
    base_urls = ''
    lists = [
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10060523',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11132401',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11004760',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10981046',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10074541',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10980985',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10916326',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10060486',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10060079',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10059863',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10060482',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11004896',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11148242',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11148239',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11458049',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11544347',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11543863',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11204118',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10949110',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10867147',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10892316',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10973188',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11534847',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10867151',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11204120',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=1025014',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11544348',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11004858',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10941415',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10941416',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=1042383',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11004900',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11500653',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10909624',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10878628',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10062689',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10009828',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10125149',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10078961',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10887996',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10960403',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10076656',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11055065',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11534851',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=1042419',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10955506',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11267301',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11593430',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10062693',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11540740',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11600625',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10909631',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11539365',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10025934',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11231672',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10023608',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11055013',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10900024',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11662837',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11273746',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11551345',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10891427',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11582385',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10119602',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11163462',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10894996',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10907983',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11579770',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11532015',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11494097',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11584550',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11133309',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11504390',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11509769',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11158207',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11517788',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11249674',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11488436',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11535250',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11262509',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11270239',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10895219',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10120984',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10179198',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10973467',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11096952',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11009946',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10975464',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11065633',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10905326',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11657606',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11510938',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10979989',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11056335',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11056335',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11085927',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11085927',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11267874',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10907242',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11559497',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11102596',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10996619',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10954992',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=11558608',
        'http://www.ireader.com/index.php?ca=bookdetail.index&bid=10175636',

    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=======================',response.url)
        # print(response.text)
        item = TCommentsPubItem()
        src_url = response.url
        item["src_url"] = src_url
        product_number = ''.join(response.xpath('//h2/a/text()').extract()).strip()
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P18'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        link = ''.join(response.xpath('//p[@class="loadMore"]/a/@href').extract()).strip()
        # print('url:',url)
        yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item}, dont_filter=True)
    def parse_page(self, response):
        print('1,==========================',response.url)
        uids = response.xpath('//a[@data-tid]/@data-tid').extract()
        # print('uids:',uids)
        for uid in uids:
            # print('uid:',uid)
            item = response.meta["item"]
            nick_name = ''.join(response.xpath('//a[@data-tid="{}"]/../preceding-sibling::div[@class="ComMan"]/p/text()'.format(uid)).extract()).strip()
            item["nick_name"] = nick_name
            # print('nick_name:',nick_name)
            cmt_date = ''.join(response.xpath('//a[@data-tid="{}"]/../preceding-sibling::div[@class="ComMan"]/span[last()]/text()'.format(uid)).extract()).strip()
            # print('cmt_date:', cmt_date)
            cmt_date = parse_time(cmt_date)
            item["cmt_date"] = cmt_date
            # print('cmt_date:',cmt_date)
            cmt_time = ''.join(response.xpath('//a[@data-tid="{}"]/../preceding-sibling::div[@class="ComMan"]/span[last()]/text()'.format(uid)).extract()).strip()
            cmt_time = parse_time(cmt_time)
            item["cmt_time"] = cmt_time
            # print('cmt_time:',cmt_time)
            comments = ''.join(response.xpath('//a[@data-tid="{}"]/../preceding-sibling::div[@class="disTxt"]/p/i/a/text()'.format(uid)).extract()).strip()
            item["comments"] = comments
            # print('comments:',comments)
            like_cnt = ''.join(response.xpath('//a[@data-tid="{}" and @class="zan click"]/i/text()'.format(uid)).extract()).strip()
            if like_cnt:
                item["like_cnt"] = like_cnt
                # print('like_cnt:',like_cnt)
            else:
                like_cnt = 0
                item["like_cnt"] = like_cnt
                # print('like_cnt:', like_cnt)
            cmt_reply_cnt = ''.join(response.xpath('//a[@data-tid="{}"]/following-sibling::a[@class="huifu"]/i/text()'.format(uid)).extract()).strip()
            if cmt_reply_cnt:
                item["cmt_reply_cnt"] = cmt_reply_cnt
                # print('cmt_reply_cnt:',cmt_reply_cnt)
            else:
                cmt_reply_cnt = 0
                item["cmt_reply_cnt"] = cmt_reply_cnt
                # print('cmt_reply_cnt:', cmt_reply_cnt)

            long_comment = 0
            item["long_comment"] = long_comment
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            print('last_modify_date:', last_modify_date)
            print('item:',item)
            yield item
            next_page_url = ''.join(response.xpath('//div[@class="changepage"]/span/a[last()]/@href').extract()).strip()
            # print(next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_page, meta={'item': item}, dont_filter=True)