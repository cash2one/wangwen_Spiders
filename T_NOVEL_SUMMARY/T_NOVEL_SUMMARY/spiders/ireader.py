# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,chinesedigits
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

class IreaderSpider(scrapy.Spider):
    name = 'ireader'
    allowed_domains = ['www.ireader.com']
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

    num_pattern = re.compile(r'\d+')

    def parse(self, response):
        print('1,=======================',response.url)
        text = response.text
        # print(text)
        item = TNovelSummaryItem()
        src_url = response.url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//div[@class="bookname"]/h2/a/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P18'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update =  ''.join(response.xpath('//div[@class="bookTit"]/div[@class="new"]/p/a/text()').extract()).strip()
        # print('Chapter_num_update:',Chapter_num_update)
        if Chapter_num_update:
            try:
                Chapter_num_update = ''.join(re.findall(u'第(.*?)章', Chapter_num_update))
                Chapter_num_update = chinesedigits(Chapter_num_update)
                item["Chapter_num_update"] = Chapter_num_update
                print('Chapter_num_update:', Chapter_num_update)
            except:
                Chapter_num_update = ''.join(re.findall(r'(\d+)', Chapter_num_update))
                item["Chapter_num_update"] = Chapter_num_update
                print('Chapter_num_update:', Chapter_num_update)
        else:
            Chapter_num_update = None
            item["Chapter_num_update"] = Chapter_num_update
            print('Chapter_num_update:',Chapter_num_update)

        update_date = ''.join(response.xpath('//div[@class="bookTit"]/div[@class="time"]/p/text()').extract()).strip()
        if update_date:
            item["update_date"] = update_date
            print('update_date:',update_date)
        else:
            update_date = datetime.datetime.now().strftime('%Y-%m-%d')
            item["update_date"] = update_date
            print('update_date:', update_date)
        words = ''.join(response.xpath('//div[@class="bookinf01"]/p/span[2]/text()').extract()).strip()
        words = process_number(words)
        item["words"] = words
        print('words:',words)
        click_num = None
        item["click_num"] = click_num
        print('click_num:',click_num)
        tickets_num = None
        item["tickets_num"] = tickets_num
        comment_num = ''.join(response.xpath('//div[@class="bookCir"]/div[@class="title"]/p/span[last()]/text()').extract()).strip()
        # print('comment_num:',comment_num)
        if '条' in comment_num:
            comment_num = comment_num.split('，')[1]
            comment_num = ''.join(re.findall(r'(.*?)条',comment_num, re.I|re.M))
            # print('comment_num:',comment_num)
            if 'w+' in comment_num:
                comment_num = process_number(comment_num)
                item["comment_num"] = comment_num
                print('comment_num:',comment_num)
            else:
                comment_num = comment_num
                item["comment_num"] = comment_num
                print('comment_num:',comment_num)
        else:
            comment_num = 0
            item["comment_num"] = comment_num
            print('comment_num:',comment_num)
        score = ''.join(response.xpath('//div[@class="bookinf01"]/div[@class="bookname"]/span/text()').extract()).strip()
        if score:
            item["score"] = score
            print('score:',score)
        else:
            score = 0
            item["score"] = score
            print('score:', score)
        collect_num = ''.join(response.xpath('//div[@class="bookinf01"]/p/span[3]/b/text()').extract()).strip()
        print('collect_num:', collect_num)
        if collect_num:
            collect_num = process_number(collect_num)
            item["collect_num"] = collect_num
            print('collect_num:',collect_num)
        else:
            collect_num = 0
            item["collect_num"] = collect_num
            print('collect_num:', collect_num)
        reward_num = None
        item["reward_num"] = reward_num
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        yield item