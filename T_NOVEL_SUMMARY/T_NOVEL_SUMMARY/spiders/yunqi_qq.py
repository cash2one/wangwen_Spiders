# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,chinesedigits,parse_time
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

class QqSpider(scrapy.Spider):
    name = 'yunqi_qq'
    allowed_domains = ['yunqi.qq.com']
    start_urls = []
    lists = [
        'http://yunqi.qq.com/bk/xdyq/20304305.html',
        'http://yunqi.qq.com/bk/gdyq/19818084.html',
        'http://yunqi.qq.com/bk/xdyq/20427349.html?sword=后来偏偏喜欢你',
        'http://yunqi.qq.com/bk/xdyq/20624146.html?sword=余生漫漫皆为你',
        'http://yunqi.qq.com/bk/gdyq/185422.html?sword=一世倾城',
        'http://yunqi.qq.com/bk/gdyq/20540647.html?sword=重生最强女帝',
        'http://yunqi.qq.com/bk/xhyq/607991.html?sword=神医弃女',
        'http://yunqi.qq.com/bk/gdyq/11758803.html?sword=天医凤九',
        'http://yunqi.qq.com/bk/xdyq/14144781.html',
        'http://yunqi.qq.com/bk/xhyq/238544.html',
        'http://yunqi.qq.com/bk/xdyq/612464.html',
        'http://yunqi.qq.com/bk/xdyq/454426.html',
        'http://yunqi.qq.com/bk/xdyq/13648272.html?sword=许你万丈光芒好',
        'http://yunqi.qq.com/bk/gdyq/236549.html?sword=绝世神偷：废柴七小姐',
        'http://yunqi.qq.com/bk/xdyq/749834.html?sword=傲娇男神住我家',
        'http://yunqi.qq.com/bk/xdyq/243535.html?sword=拒嫁天王老公',
        'http://yunqi.qq.com/bk/xdyq/13700974.html?sword=那时喜欢你',
        'http://yunqi.qq.com/bk/gdyq/626275.html',
        'http://yunqi.qq.com/bk/xdyq/233707.html?sword=誓不为妻：全球豪娶少夫人',
        'http://yunqi.qq.com/bk/xhyq/317796.html?sword=纨绔仙医：邪帝毒爱妃',
        'http://yunqi.qq.com/bk/xdyq/16204776.html?sword=亿万星辰不及你',
        'http://yunqi.qq.com/bk/xdyq/234538.html?sword=他来了，请闭眼',
        'http://yunqi.qq.com/bk/xdyq/234538.html?sword=有123456',
        'http://yunqi.qq.com/bk/xdyq/234538.html?sword=如果蜗牛有爱情',

    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,========================',response.url)
        text = response.text
        # print(text)
        item = TNovelSummaryItem()
        url = response.url
        src_url = url
        item["src_url"] = src_url
        print('src_url:', src_url)
        product_number = ''.join(response.xpath('//img[@class="qqredaer_tit"]/@title').extract()).strip()
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P17'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update_s = ''.join(response.xpath('//*[@id="newChapterList"]/div[@class="chaptername"]/b/a[@class="green"]/text()').extract()).strip()
        print('Chapter_num_update_s:', Chapter_num_update_s)
        if Chapter_num_update_s:
            Chapter_num_update = ''.join(re.findall(u'第.*?卷 第([\u4e00-\u9fa5]{4,10})\s', Chapter_num_update_s, re.I | re.M))
            if Chapter_num_update:
                Chapter_num_update = chinesedigits(Chapter_num_update)
                item["Chapter_num_update"] = Chapter_num_update
                print('Chapter_num_update:', Chapter_num_update)
            else:
                Chapter_num_update = ''.join(re.findall(r'第(\d+)章',Chapter_num_update_s, re.I|re.M))
                if Chapter_num_update:
                    item["Chapter_num_update"] = Chapter_num_update
                    print('Chapter_num_update:', Chapter_num_update)
                else:
                    Chapter_num_update = ''.join(re.findall(r'第.*?卷 (\d+)',Chapter_num_update_s, re.I|re.M))
                    if Chapter_num_update:
                        item["Chapter_num_update"] = Chapter_num_update
                        print('Chapter_num_update:', Chapter_num_update)
                    else:
                        Chapter_num_update = ''.join(re.findall(r'第.*?卷 \【(.*?)\】', Chapter_num_update_s, re.I | re.M))
                        if Chapter_num_update:
                            item["Chapter_num_update"] = Chapter_num_update
                            print('Chapter_num_update:', Chapter_num_update)
                        else:
                            Chapter_num_update = ''.join(re.findall(r'第.*?卷 [\u4e00-\u9fa5]{0,6}\（(\d+)\）', Chapter_num_update_s, re.I | re.M))
                            if Chapter_num_update:
                                item["Chapter_num_update"] = Chapter_num_update
                                print('Chapter_num_update:', Chapter_num_update)
                            else:
                                Chapter_num_update = None
                                item["Chapter_num_update"] = Chapter_num_update
                                print('Chapter_num_update:', Chapter_num_update)
        else:
            Chapter_num_update = None
            item["Chapter_num_update"] = Chapter_num_update
            print('Chapter_num_update:', Chapter_num_update)


        update_date = ''.join(response.xpath('//*[@id="newChapterList"]/div[@class="chaptername"]/text()').extract()).strip()
        if update_date:
            update_date = update_date.replace('(更新时间：','').replace(')','')
        else:
            update_date = datetime.datetime.now().strftime('%Y-%m-%d')
        item["update_date"] = update_date
        print('update_date:',update_date)
        words = ' '.join(response.xpath('//div[@class="num"]/table/tr/td/text()').extract()).strip()
        if words:
            words = ''.join(re.findall(r'总字数：(\d+)',words, re.I|re.M))
        else:
            words = None
        item["words"] = words
        print('words:',words)
        click_num = ' '.join(response.xpath('//div[@class="num"]/table/tr/td/text()').extract()).strip()
        if click_num:
            click_num = ''.join(re.findall(r'阅文点击：(\d+)',click_num, re.I|re.M))
        else:
            click_num = None
        item["click_num"] = click_num
        print('click_num:',click_num)
        score = None
        item["score"] = score
        collect_num = None
        item["collect_num"] = collect_num
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        bid = ''.join(re.findall(r'\/(\d+).html',url, re.I|re.M))
        print('bid:',bid)
        link = 'http://yunqi.qq.com/novelcomment/index.html?bid={}'.format(bid)
        yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item,'bid':bid}, dont_filter=True)
    def parse_page(self,response):
        print('2,=====================',response.url)
        item= response.meta["item"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print(jsons)
        comment_num = jsons.get('data').get('commentNum')
        if comment_num:
            item["comment_num"] = comment_num
            print('comment_num:',comment_num)
        else:
            comment_num = 0
            item["comment_num"] = comment_num
            print('comment_num:', comment_num)
        bid = response.meta["bid"]
        link = 'http://yunqi.qq.com/novel/interactCenter.html?bid={}'.format(bid)
        yield scrapy.Request(url=link, callback=self.parse_page_s, meta={'item': item}, dont_filter=True)
    def parse_page_s(self,response):
        print('3,========================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print(jsons)
        content = jsons.get('content')
        if  content:
            # print(content)
            sel = etree.HTML(content)
            # print(sel)
            tickets_num = ''.join(sel.xpath('//*[@id="swishnev001"]/div[@class="sw_left"]/ul/li/b[@class="bts"]/span/text()'))
            item["tickets_num"] = tickets_num
            print('tickets_num:',tickets_num)
        else:
            tickets_num = 0
            item["tickets_num"] = tickets_num
            print('tickets_num:', tickets_num)
        reward_num = None
        item["reward_num"] = reward_num
        print('item:',item)
        yield item






