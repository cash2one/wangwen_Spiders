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

class JjwxcSpider(scrapy.Spider):
    name = 'jjwxc'
    allowed_domains = ['www.jjwxc.net']
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
        'http://www.jjwxc.net/onebook.php?novelid=3200611',
        'http://www.jjwxc.net/onebook.php?novelid=3433838',
        'http://www.jjwxc.net/onebook.php?novelid=3200611'
        ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=====================',response.url)
        item = TCommentsPubItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        novelid = src_url.replace('http://www.jjwxc.net/onebook.php?novelid=','')
        print('novelid:',novelid)
        product_number = ''.join(response.xpath('//h1[@itemprop="name"]/span/text()').extract()).strip()
        print('product_number:', product_number)
        # product_number = get_product_number(product_number)
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
        # print('product_number:', product_number)
        # item["product_number"] = product_number
        plat_number = 'P16'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        j_url = 'http://s8-static.jjwxc.net/comment_json.php?novelid={}'.format(novelid)
        # print('j_url:',j_url)
        yield scrapy.Request(url=j_url, callback=self.parse_page, meta={'item': item}, dont_filter=True)

        link = 'http://www.jjwxc.net/comment.php?novelid={}&huati=1&page=1'.format(novelid)
        print('link:',link)
        yield scrapy.Request(url=link, callback=self.parse_page_url, meta={'item': item}, dont_filter=True)
    def parse_page(self,response):
        print('2,==================',response.url)
        item = response.meta["item"]
        jsons = response.text
        # print('jsons:',type(jsons))
        jsons = json.loads(jsons)
        # print('jsons:',type(jsons))
        body = jsons.get('body')
        # print(body)
        for bd in body:
            # print(type(bd))
            nick_name = bd.get('commentauthor')
            item["nick_name"] = nick_name
            print('nick_name:',nick_name)
            cmt_date = bd.get('commentdate')
            cmt_date = cmt_date.split(' ')[0]
            item["cmt_date"] = cmt_date
            print('cmt_date:',cmt_date)
            cmt_time = bd.get('commentdate')
            item["cmt_time"] = cmt_time
            print('cmt_time:',cmt_time)
            comments = bd.get('commentbody')
            bq = re.compile(r'<(S*?)[^>]*>.*?|<.*? />', re.I)
            # 去掉HTML标签
            comments = bq.sub('', comments).strip()
            item["comments"] = comments
            print('comments:',comments)
            like_cnt = None
            item["like_cnt"] = like_cnt
            # print('like_cnt:',like_cnt)
            cmt_reply_cnt = bd.get('reply_total')
            item["cmt_reply_cnt"] = cmt_reply_cnt
            print('cmt_reply_cnt:',cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            yield item
    def parse_page_url(self,response):
        print('3,===================', response.url)
        url = response.url
        novelid = ''.join(re.findall(r'novelid=\d+', url)).strip().replace('novelid=', '')
        print('novelid:', novelid)
        item = response.meta["item"]
        lpage = ''.join(response.xpath('//div[@class="pagebar"]/a[last()]/@href').extract()).strip()
        page = ''.join(re.findall(r'page=\d+', lpage)).strip().replace('page=', '')
        for p in range(1, int(page)):
            # print('page:',page)
            url = 'http://www.jjwxc.net/comment.php?novelid={}&huati=1&page={}'.format(novelid, p)
            # print(url)
            yield scrapy.Request(url=url, callback=self.parse_new_page, meta={'item': item}, dont_filter=True)
    def parse_new_page(self,response):
        print('4,===================',response.url)
        data_commentid = response.xpath('//div[@id and @data-commentid]/@data-commentid').extract()
        # print('data_commentid:',data_commentid)
        for uid in data_commentid:
            # print(uid)
            item = response.meta["item"]
            nick_name = ''.join(response.xpath('//div[@id="comment_{}"]/div[@class="readtd"]/div[@class="tdtitle"]/span[@class="coltext"]/span[@class="blacktext"]/a/text()'.format(uid)).extract()).strip()
            item["nick_name"] = nick_name
            print('nick_name:',nick_name)
            cmt_date = ''.join(response.xpath('//div[@id="comment_{}"]/div[@class="readtd"]/div[@class="tdtitle"]/span[@class="coltext"]//text()'.format(uid)).extract()).strip()
            # print('cmt_date:', cmt_date)
            if "发表时间：" in cmt_date:
                cmt_date = re.findall(r'发表时间：[\d+]{4}-[\d+]{2}-[\d+]{2}',cmt_date)
                item["cmt_date"] = ''.join(cmt_date).replace('发表时间：','')
                print('cmt_date:',item["cmt_date"])
            cmt_time = ''.join(response.xpath('//div[@id="comment_{}"]/div[@class="readtd"]/div[@class="tdtitle"]/span[@class="coltext"]//text()'.format(uid)).extract()).strip()
            # print('cmt_time:',cmt_time)
            if "发表时间：" in cmt_time:
                cmt_time = re.findall(r'发表时间：[\d+]{4}-[\d+]{2}-[\d+]{2}\s[\d+]{2}\:[\d+]{2}\:[\d+]{2}', cmt_time)
                item["cmt_time"] = ''.join(cmt_time).replace('发表时间：','')
                print('cmt_time:', item["cmt_time"])
            comments = ''.join(response.xpath('//div[@id="comment_{}"]/div[@class="readtd"]/div[@class="readbody"]/text()'.format(uid)).extract()).strip()
            item["comments"] = comments
            print('comments:',comments)
            like_cnt = None
            item["like_cnt"] = like_cnt
            cmt_reply_cnt = ''.join(response.xpath('//div[@id="comment_{}"]/div[@class="readtd"]/div[@class="replycontent"]/div[last()]/text()'.format(uid)).extract()).strip()
            cmt_reply_cnt = ''.join(re.findall(r'\[\d+楼\]',cmt_reply_cnt)).strip().replace('[','').replace('楼]','')
            if cmt_reply_cnt:
                cmt_reply_cnt = int(cmt_reply_cnt)
                item["cmt_reply_cnt"] = cmt_reply_cnt
                print('cmt_reply_cnt:',cmt_reply_cnt)
            else:
                cmt_reply_cnt = 0
                item["cmt_reply_cnt"] = cmt_reply_cnt
                print('cmt_reply_cnt:', cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            yield item

