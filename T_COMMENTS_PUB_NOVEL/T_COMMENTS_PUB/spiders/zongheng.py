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

class ZonghengSpider(scrapy.Spider):
    name = 'zongheng'
    allowed_domains = ['book.zongheng.com']
    start_urls = []
    base_urls = ''
    lists = [
         'http://book.zongheng.com/book/603738.html',
        'http://book.zongheng.com/book/523438.html',
        'http://book.zongheng.com/book/555035.html',
        'http://book.zongheng.com/book/568097.html',
        'http://book.zongheng.com/book/632434.html',
        'http://book.zongheng.com/book/635570.html',
        'http://book.zongheng.com/book/43467.html',
        'http://book.zongheng.com/book/682920.html',
        'http://book.zongheng.com/book/685640.html',
        'http://book.zongheng.com/book/512263.html',
        'http://book.zongheng.com/book/309318.html',
        'http://book.zongheng.com/book/457529.html',
        'http://book.zongheng.com/book/594492.html',
        'http://book.zongheng.com/book/342974.html',
        'http://book.zongheng.com/book/730066.html',
        'http://book.zongheng.com/book/510426.html',
        'http://book.zongheng.com/book/411993.html',
        'http://book.zongheng.com/book/45669.html',
        'http://book.zongheng.com/book/665301.html',
        'http://book.zongheng.com/book/401153.html',
        'http://book.zongheng.com/book/408586.html',
        'http://book.zongheng.com/book/481225.html',
        'http://book.zongheng.com/book/472101.html',
        'http://book.zongheng.com/book/431658.html',
        'http://book.zongheng.com/book/390470.html',
        'http://book.zongheng.com/book/524571.html',
        'http://book.zongheng.com/book/158432.html',
        'http://book.zongheng.com/book/688697.html',
        'http://book.zongheng.com/book/512648.html',
        'http://book.zongheng.com/book/470711.html',
        'http://book.zongheng.com/book/458842.html',
        'http://book.zongheng.com/book/189169.html',
        'http://book.zongheng.com/book/490372.html',
        'http://book.zongheng.com/book/435710.html',
        'http://book.zongheng.com/book/672340.html',
        'http://book.zongheng.com/book/47364.html',
        'http://book.zongheng.com/book/431145.html',
        'http://book.zongheng.com/book/280744.html',
        'http://book.zongheng.com/book/390021.html',
        'http://book.zongheng.com/book/251393.html',
        'http://book.zongheng.com/book/175703.html',
        'http://book.zongheng.com/book/570946.html',
        'http://book.zongheng.com/book/290053.html',
        'http://book.zongheng.com/book/525936.html',
        'http://book.zongheng.com/book/311835.html',
        'http://book.zongheng.com/book/732001.html',
        'http://book.zongheng.com/book/591444.html',
        'http://book.zongheng.com/book/69507.html',
        'http://book.zongheng.com/book/390199.html',
        'http://book.zongheng.com/book/347511.html',
        'http://book.zongheng.com/book/468543.html',
        'http://book.zongheng.com/book/472776.html',
        'http://book.zongheng.com/book/296950.html',
        'http://book.zongheng.com/book/513438.html',
        'http://book.zongheng.com/book/205411.html',
        'http://book.zongheng.com/book/121112.html',
        'http://book.zongheng.com/book/639927.html',
        'http://book.zongheng.com/book/88463.html',
        'http://book.zongheng.com/book/56579.html',
        'http://book.zongheng.com/book/568980.html',
        'http://book.zongheng.com/book/612328.html',
        'http://book.zongheng.com/book/676518.html',
        'http://book.zongheng.com/book/262883.html',
        'http://book.zongheng.com/book/720864.html',
        'http://book.zongheng.com/book/708632.html',
        'http://book.zongheng.com/book/377897.html',
        'http://book.zongheng.com/book/352542.html',
        'http://book.zongheng.com/book/646519.html',
        'http://book.zongheng.com/book/572891.html',
        'http://book.zongheng.com/book/36788.html',
        'http://book.zongheng.com/book/65189.html',
        'http://book.zongheng.com/book/578824.html',
        'http://book.zongheng.com/book/205836.html',
        'http://book.zongheng.com/book/714691.html',
        'http://book.zongheng.com/book/156062.html',
        'http://book.zongheng.com/book/450702.html',
        'http://book.zongheng.com/book/362880.html',
        'http://book.zongheng.com/book/645062.html',
        'http://book.zongheng.com/book/384410.html',

    ]

    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,===============',response.url)
        html = response.text
        item = TCommentsPubItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(re.findall(r'bookName\=\"(.*)\"',html)).strip().replace('bookName="','').replace('"','')
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P21'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        long_comment = 0
        item["long_comment"] = long_comment
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        bookId = ''.join(re.findall(r'bookId=\"\d+\"',html)).strip().replace('bookId="','').replace('"','')
        # print('bookId:',bookId)
        url = 'http://book.zongheng.com/api/book/comment/getThreadL1st2.htm'
        formdata = {
            'bookId': bookId,
            'pagebar': '1',
            'pageNum': '1',
            'pageSize': '30',
        }
        # FormRequest 是Scrapy发送POST请求的方法
        yield scrapy.FormRequest(
            url=url,
            formdata=formdata,
            callback=self.parse_page_p,
            meta={'item': item, 'bookId': bookId},
            dont_filter=True,
        )

    def parse_page_p(self, response):
        print('2,======================', response.url)
        item = response.meta["item"]
        bookId = response.meta["bookId"]
        html = response.text
        # print(html)
        page = ''.join(response.xpath('//div[@class="page"]/div[@class="pagenumber pagebar"]/@count').extract()).strip()
        print('page:', page)
        url = 'http://book.zongheng.com/api/book/comment/getThreadL1st2.htm'
        for p in range(1, int(page) + 1):
            formdata = {
                'bookId': bookId,
                'pagebar': '1',
                'pageNum': str(p),
                'pageSize': '30',
            }
            # FormRequest 是Scrapy发送POST请求的方法
            yield scrapy.FormRequest(
                url=url,
                formdata=formdata,
                callback=self.parse_page,
                meta={'item': item},
                dont_filter=True,
            )

    def parse_page(self, response):
        print('3,===========================',response.url)
        html = response.text
        # print(html)
        threadId = response.xpath('//div[@class="comment"]/div[@class="comment_wz"]/h4[@threadid]/@threadid').extract()
        # print('threadId:',threadId)
        for uid in threadId:
            print('uid=============:',uid)
            item = response.meta["item"]
            print('item:', item)
            nick_name = ''.join(response.xpath('//div[@class="comment"]/div[@class="comment_wz"]/h4[@threadid="{}"]/following-sibling::div[@class="wz"]/p[@class="wz_fb"]/a/em[@class="z_u"]/text()'.format(uid)).extract()).strip()
            # print('nick_name:', nick_name)
            item["nick_name"] = nick_name
            cmt_date = ''.join(response.xpath('//div[@class="comment"]/div[@class="comment_wz"]/h4[@threadid="{}"]/following-sibling::div[@class="comment_rw"]/span[@class="fl"]/em/text()'.format(uid)).extract()).strip()
            item["cmt_date"] = cmt_date
            # print('cmt_date:', cmt_date)
            cmt_time = ''.join(response.xpath('//div[@class="comment"]/div[@class="comment_wz"]/h4[@threadid="{}"]/following-sibling::div[@class="comment_rw"]/span[@class="fl"]/em/text()'.format(uid)).extract()).strip()
            item["cmt_time"] = cmt_time
            # print('cmt_time:', cmt_time)
            comments = ''.join(response.xpath('//div[@class="comment"]/div[@class="comment_wz"]/h4[@threadid="{}"]/following-sibling::div[@class="wz"]/p[position()>1]//text()'.format(uid)).extract()).strip().replace('[收起]','')
            bq = re.compile(r'[a-zA-z]+://[^\s]*', re.I)
            # 去掉HTML标签
            comments = bq.sub('', comments).strip()
            item["comments"] = comments
            # print('comments:', comments)
            like_cnt = ''.join(response.xpath('//div[@class="comment"]/div[@class="comment_wz"]/h4[@threadid="{}"]/following-sibling::div[@class="comment_rw"]/div[@class="reply"]/span[last()]/text()'.format(uid)).extract()).strip().replace('[','').replace(']','')
            item["like_cnt"] = like_cnt
            # print('like_cnt:',like_cnt)
            cmt_reply_cnt = ''.join(response.xpath('//div[@class="comment"]/div[@class="comment_wz"]/h4[@threadid="{}"]/following-sibling::div[@class="comment_rw"]/div[@class="reply"]/span[last()-1]/em/text()'.format(uid)).extract()).strip().replace('[','').replace(']','')
            item["cmt_reply_cnt"] = cmt_reply_cnt
            # print('cmt_reply_cnt:', cmt_reply_cnt)
            yield item

