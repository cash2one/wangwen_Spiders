
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
    name = 'chuangshi_qq'
    allowed_domains = ['chuangshi.qq.com']
    start_urls = []
    lists = [
        'http://chuangshi.qq.com/bk/xh/349652.html?sword=焚天之怒',
        'http://chuangshi.qq.com/bk/ds/161342.html?sword=校花之贴身高手',
        'http://chuangshi.qq.com/bk/ds/19915605.html?sword=奶爸的文艺人生',
        'http://chuangshi.qq.com/bk/yx/216351.html?sword=联盟之谁与争锋',
        'http://chuangshi.qq.com/bk/xh/433109.html?sword=战神无敌',
        'http://chuangshi.qq.com/bk/xx/465030.html?sword=凡人修仙传',
        'http://chuangshi.qq.com/bk/yx/478670.html?sword=全职高手',
        'http://chuangshi.qq.com/bk/xx/475863.html?sword=遮天',
        'http://chuangshi.qq.com/bk/kh/503075.html?sword=异常生物见闻录',
        'http://chuangshi.qq.com/bk/ls/14175804.html?sword=逍遥小书生',
        'http://chuangshi.qq.com/bk/ds/832298.html?sword=重生之财源滚滚',
        'http://chuangshi.qq.com/bk/js/295037.html',
        'http://chuangshi.qq.com/bk/xh/481126.html?sword=武动乾坤',
        'http://chuangshi.qq.com/bk/xx/462522.html?sword=莽荒纪',
        'http://chuangshi.qq.com/bk/xh/462521.html?sword=完美世界',
        'http://chuangshi.qq.com/bk/xh/462523.html?sword=大主宰',
        'http://chuangshi.qq.com/bk/xh/15238666.html?sword=万界天尊',
        'http://chuangshi.qq.com/bk/ls/488347.html?sword=唐砖',
        'http://chuangshi.qq.com/bk/qc/215913.html?sword=余罪',
        'http://chuangshi.qq.com/bk/xh/462952.html?sword=将夜',
        'http://chuangshi.qq.com/bk/xx/485272.html?sword=最强弃少',
        'http://chuangshi.qq.com/bk/yx/222407.html?sword=穿越火线之AK传奇',
        'http://chuangshi.qq.com/bk/xh/14179514.html?sword=天道图书馆',
        'http://chuangshi.qq.com/bk/ds/479232.html?sword=校花的贴身高手',
        'http://chuangshi.qq.com/bk/xh/14608738.html?sword=圣墟',
        'http://chuangshi.qq.com/bk/ls/480068.html?sword=赘婿',
        'http://chuangshi.qq.com/bk/xx/819435.html?sword=一念永恒',
        'http://chuangshi.qq.com/bk/ds/20191960.html?sword=大王饶命',
        'http://chuangshi.qq.com/bk/xx/20468795.html?sword=飞剑问道',
        'http://chuangshi.qq.com/bk/ds/789906.html?sword=修真聊天群',
        'http://chuangshi.qq.com/bk/xx/20734492.html?sword=凡人修仙之仙界篇',
        'http://chuangshi.qq.com/bk/xh/19704712.html?sword=牧神记',
        'http://chuangshi.qq.com/bk/xh/804453.html?sword=斗罗大陆III龙王传说',
        'http://chuangshi.qq.com/bk/ls/20136878.html?sword=汉乡',
        'http://chuangshi.qq.com/bk/xh/462597.html?sword=帝霸',
        'http://chuangshi.qq.com/bk/xh/489745.html?sword=武炼巅峰',
        'http://chuangshi.qq.com/bk/ls/14185492.html?sword=带着仓库到大明',
        'http://chuangshi.qq.com/bk/ds/13541158.html?sword=我的1979',
        'http://chuangshi.qq.com/bk/xx/484840.html?sword=大道争锋',
        'http://chuangshi.qq.com/bk/xh/20399782.html?sword=太初',
        'http://chuangshi.qq.com/bk/xh/20868264.html?sword=诡秘之主',
        'http://chuangshi.qq.com/bk/qh/817386.html?sword=放开那个女巫',
        'http://chuangshi.qq.com/bk/ds/305138.html',
        'http://chuangshi.qq.com/bk/xh/263991.html',
        'http://chuangshi.qq.com/bk/ds/356087.html',
        'http://chuangshi.qq.com/bk/xh/353221.html',
        'http://chuangshi.qq.com/bk/ds/499686.html',

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
                if '章' in Chapter_num_update:
                    Chapter_num_update = Chapter_num_update.replace('章','')
                    Chapter_num_update = chinesedigits(Chapter_num_update)
                    item["Chapter_num_update"] = Chapter_num_update
                    print('Chapter_num_update:', Chapter_num_update)
                else:
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
                        Chapter_num_update = ''.join(re.findall(r'第.*?卷 \【(\d+)\】', Chapter_num_update_s, re.I | re.M))
                        if Chapter_num_update:
                            item["Chapter_num_update"] = Chapter_num_update
                            print('Chapter_num_update:', Chapter_num_update)
                        else:
                            Chapter_num_update = ''.join(re.findall(r'第.*?卷 [\u4e00-\u9fa5]{0,6}\（(\d+)\）', Chapter_num_update_s, re.I | re.M))
                            if Chapter_num_update:
                                item["Chapter_num_update"] = Chapter_num_update
                                print('Chapter_num_update:', Chapter_num_update)
                            else:
                                Chapter_num_update = ''.join(re.findall(u'第.*?卷 第([\u4e00-\u9fa5]{1,10})章', Chapter_num_update_s, re.I | re.M))
                                if Chapter_num_update:
                                    Chapter_num_update = chinesedigits(Chapter_num_update)
                                    item["Chapter_num_update"] = Chapter_num_update
                                    print('Chapter_num_update:', Chapter_num_update)
                                else:
                                    Chapter_num_update = ''.join(re.findall(u'第([\u4e00-\u9fa5]{1,10})章', Chapter_num_update_s,re.I | re.M))
                                    if Chapter_num_update:
                                        Chapter_num_update = chinesedigits(Chapter_num_update)
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
            update_date = None
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
        link = 'http://chuangshi.qq.com/novelcomment/index.html?bid={}'.format(bid)
        yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item,'bid':bid}, dont_filter=True)
    def parse_page(self,response):
        print('2,=====================',response.url)
        item= response.meta["item"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print(jsons)
        comment_num = jsons.get('data').get('commentNum')
        item["comment_num"] = comment_num
        print('comment_num:',comment_num)
        bid = response.meta["bid"]
        link = 'http://chuangshi.qq.com/novel/interactCenter.html?bid={}'.format(bid)
        yield scrapy.Request(url=link, callback=self.parse_page_s, meta={'item': item}, dont_filter=True)
    def parse_page_s(self,response):
        print('3,========================',response.url)
        item = response.meta["item"]
        text = response.text
        # print(text)
        jsons = json.loads(text)
        # print(jsons)
        content = jsons.get('content')
        # print(content)
        sel = etree.HTML(content)
        # print(sel)
        tickets_num = ''.join(sel.xpath('//*[@id="swishnev001"]/div[@class="sw_left"]/ul/li/b[@class="bts"]/span/text()'))
        if tickets_num:
            item["tickets_num"] = tickets_num
            print('tickets_num:',tickets_num)
        else:
            tickets_num = 0
            item["tickets_num"] = tickets_num
            print('tickets_num:', tickets_num)
        reward_num = None
        item["reward_num"] = reward_num
        yield item






