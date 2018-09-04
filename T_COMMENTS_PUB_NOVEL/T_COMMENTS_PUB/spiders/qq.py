# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_COMMENTS_PUB.items import TCommentsPubItem
from T_COMMENTS_PUB.utils.get_product_number import get_product_number
from T_COMMENTS_PUB.utils.process import process_date,process_number, parse_time
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

class QqSpider(scrapy.Spider):
    name = 'qq'
    # allowed_domains = ['chuangshi.qq.com']
    start_urls = []
    base_urls = ''
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
        'http://chuangshi.qq.com/bk/ds/305138.html',
        'http://chuangshi.qq.com/bk/xh/263991.html',
        'http://chuangshi.qq.com/bk/ds/356087.html',
        'http://chuangshi.qq.com/bk/xh/353221.html',
        'http://chuangshi.qq.com/bk/ds/499686.html',
        'http://yunqi.qq.com/bk/xdyq/234538.html?sword=他来了，请闭眼',
        'http://yunqi.qq.com/bk/xdyq/234538.html?sword=有123456',
        'http://yunqi.qq.com/bk/xdyq/234538.html?sword=如果蜗牛有爱情',
    ]

    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,========================',response.url)
        html = response.text
        # print(html)
        item = TCommentsPubItem()
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
        link = ''.join(response.xpath('//div[@class="tablist"]/ul/li/a[contains(text(),"评论")]/@href').extract()).strip()
        print('link:',link)
        yield scrapy.Request(url=link, callback=self.parse_page_link, meta={'item': item},dont_filter=True)

    def parse_page_link(self,response):
        print('2,============================',response.url)
        item = response.meta["item"]
        html = response.text
        # print(response.text)
        pageInput = ''.join(re.findall(r'pageInput=(\d+)',html))
        print('pageInput:',pageInput)
        for page in range(1,int(pageInput)+1):
            link = response.url + '?hot=0&p={}'.format(page)
            # print('link:',link)
            yield scrapy.Request(url=link, callback=self.parse_page, meta={'item': item}, dont_filter=True)
    def parse_page(self, response):
        print('3,=========================',response.url)
        html = response.text
        # print(html)
        uids = response.xpath('//ul[@id="commentList"]/li/@id').extract()
        # print('uids:',uids)
        for id in uids:
            # print('id:',id)
            item = response.meta["item"]
            nick_name = ''.join(response.xpath('//*[@id="{}"]/div[@class="userComment"]/p/a/text()'.format(id)).extract()).strip()
            # print('nick_name:', nick_name)
            item["nick_name"] = nick_name
            cmt_date = ''.join(response.xpath('//*[@id="{}"]/div[@class="userComment"]/p/span/text()'.format(id)).extract()).strip().replace('发布','')
            cmt_date = parse_time(cmt_date).split(' ')[0]
            item["cmt_date"] = cmt_date
            # print('cmt_date:', cmt_date)
            cmt_time_s = ''.join(response.xpath('//*[@id="{}"]/div[@class="userComment"]/p/span/text()'.format(id)).extract()).replace(' 发布','')
            # print('cmt_time_s:',cmt_time_s)
            cmt_time = time.strptime(cmt_time_s, "%Y-%m-%d %H:%M")
            cmt_time = time.strftime("%Y-%m-%d %H:%M:%S", cmt_time)
            item["cmt_time"] = cmt_time
            # print('cmt_time:', cmt_time)
            comments = ''.join(response.xpath('//*[@id="{}"]/div[@class="userComment"]/div[@class="packUpBox"]/div[@nodetype="commentSummaryBox"]/text()'.format(id)).extract()).strip()
            item["comments"] = comments
            # print('comments:', comments)
            like_cnt = None
            item["like_cnt"] = like_cnt
            cmt_reply_cnt = ''.join(response.xpath('//*[@id="{}"]/div[@class="userComment"]/div[@class="packUpBar cf"]/div[@class="fl"]/span[@class="replyTotal"]/a/span/text()'.format(id)).extract()).strip()
            item["cmt_reply_cnt"] = cmt_reply_cnt
            # print('cmt_reply_cnt:', cmt_reply_cnt)
            long_comment = 0
            item["long_comment"] = long_comment
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            # print('last_modify_date:', last_modify_date)
            print('item:',item)
            yield item