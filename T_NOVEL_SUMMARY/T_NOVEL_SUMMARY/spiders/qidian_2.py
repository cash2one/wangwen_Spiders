
# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,chinesedigits,parse_time
from T_NOVEL_SUMMARY.utils.words import get_words
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
import socket
from fontTools.ttLib import TTFont
from parsel import Selector
from html import unescape
import demjson


class QidianSpider(scrapy.Spider):
    name = 'qidian_2'
    allowed_domains = ['book.qidian.com']
    start_urls = [
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
        'https://book.qidian.com/info/1010468795',
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

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        print('1,=================',response.url)
        text = response.text
        # with open('qidian.txt', "wb") as f:  # 开始写文件，wb代表写二进制文件
        #     f.write(response.body)
        url = response.url
        item = TNovelSummaryItem()
        src_url = url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//h1/em/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        item["product_number"] = product_number
        print('product_number:', product_number)
        plat_number = 'P20'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        tickets_num = ''.join(response.xpath('//*[@id="monthCount"]/text()').extract()).strip()
        item["tickets_num"] = tickets_num
        print('tickets_num:', tickets_num)
        reward_num = ''.join(response.xpath('//*[@id="rewardNum"]/text()').extract()).strip()
        item["reward_num"] = reward_num
        print('reward_num:', reward_num)
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        font_type = ''.join(response.xpath('//div[@class="book-info "]/p/em[1]/span[@class]/@class').extract()).strip()
        print('font_type:', font_type)
        font_url = 'https://qidian.gtimg.com/qd_anti_spider/{}.woff'.format(font_type)
        print('font_url:', font_url)
        words = re.findall(r'</style><span class="{}">(.*)</span></em><cite>万字</cite><i>|</i><em><style>'.format(font_type), response.text, re.I|re.M)[0]
        print('words:',words)
        words = get_words(words,font_url)
        words = int(float(words)*10000)
        item["words"] = words
        print('words:', words)
        click_num = re.findall(r'</style><span class="{}">(.*)</span></em><cite>万总会员点击<span>'.format(font_type), response.text, re.I|re.M)[0]
        click_num = re.findall(r'</style><span class="{}">(.*)'.format(font_type), click_num, re.I|re.M)[0]
        print('click_num:',click_num)
        click_num = get_words(click_num, font_url)
        click_num = int(float(click_num)*10000)
        item["click_num"] = click_num
        print('click_num:',click_num)
        update_date = ''.join(response.xpath('//li[@class="update"]/div[@class="detail"]/p[@class="cf"]/em/text()').extract()).strip()
        update_date = parse_time(update_date)
        item["update_date"] = update_date
        print('update_date:',update_date)
        collect_num = None
        item["collect_num"] = collect_num
        authorId = ''.join(response.xpath('//*[@id="authorId"]/@data-authorid').extract()).strip()
        print('authorId:', authorId)
        chanId = re.findall(r'chanId\=(\d+)', text)[0]
        print('chanId:', chanId)
        bookId = ''.join(re.findall(r'https\:\/\/book\.qidian\.com\/info\/(\d+)', url, re.I | re.M))
        print('bookId:', bookId)
        _csrfToken = 'HUc4mzWMTveOYkK01P9mREV04r5f0zisvnDNZl7j'
        link = 'https://book.qidian.com/ajax/comment/index?_csrfToken=HUc4mzWMTveOYkK01P9mREV04r5f0zisvnDNZl7j&bookId={}&pageSize=15'.format(bookId)

        yield scrapy.Request(url=link, callback=self.parse_page_score,
                             meta={'item': item, 'authorId': authorId, 'chanId': chanId, 'bookId': bookId},
                            dont_filter=True)

    def parse_page_score(self, response):
        print('2,=======================', response.url)
        item = response.meta["item"]
        authorId = response.meta["authorId"]
        chanId = response.meta["chanId"]
        bookId = response.meta["bookId"]
        responses = requests.get(response.url)
        if responses.status_code == 200:
            responses.encoding = "utf-8"
            responses.content.decode()
            content = responses.json()
            # print(type(content))
            # print(content)
            score = content.get('data').get('rate')
            item["score"] = score
            print('score:', score)
        else:
            yield scrapy.Request(url=response.url, callback=self.parse_page_score,
                                 meta={'item': item, 'authorId': authorId, 'chanId': chanId, 'bookId': bookId},
                                 dont_filter=False)

        link = 'https://book.qidian.com/ajax/book/GetBookForum?_csrfToken=HUc4mzWMTveOYkK01P9mREV04r5f0zisvnDNZl7j&authorId={}&bookId={}&chanId={}&pageSize=15'.format(
            authorId, bookId, chanId)
        yield scrapy.Request(url=link, callback=self.parse_page_comment_num,
                             meta={'item': item, 'authorId': authorId, 'chanId': chanId, 'bookId': bookId},
                             dont_filter=True)

    def parse_page_comment_num(self, response):
        print('3,==========================', response.url)
        item = response.meta["item"]
        bookId = response.meta["bookId"]
        responses = requests.get(response.url)
        if responses.status_code == 200:
            # responses.encoding = responses.apparent_encoding
            responses.encoding = "utf-8"
            responses.content.decode()
            content = responses.json()
            # print(type(content))
            # print(content)
            comment_num = content.get('data').get('threadCnt')
            if comment_num:
                item["comment_num"] = comment_num
                print('comment_num:', comment_num)
            else:
                comment_num = 0
                item["comment_num"] = comment_num
                print('comment_num:', comment_num)
        link = 'https://book.qidian.com/ajax/book/category?_csrfToken=HUc4mzWMTveOYkK01P9mREV04r5f0zisvnDNZl7j&bookId={}'.format(bookId)
        yield scrapy.Request(url=link, callback=self.parse_page_Chapter_num,
                             meta={'item': item, 'bookId': bookId},
                             dont_filter=True)
    def parse_page_Chapter_num(self, response):
        print('4,=========================',response.url)
        item = response.meta["item"]
        responses = requests.get(response.url)
        if responses.status_code == 200:
            # responses.encoding = responses.apparent_encoding
            responses.encoding = "utf-8"
            responses.content.decode()
            content = responses.json()
            # print(type(content))
            # print(content)
            Chapter_num_update = content.get('data').get('chapterTotalCnt')
            item["Chapter_num_update"] = Chapter_num_update
            print('Chapter_num_update:', Chapter_num_update)
            yield item






