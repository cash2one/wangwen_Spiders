# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy.selector import Selector
from T_NOVEL_SUMMARY.items import TNovelSummaryItem
from T_NOVEL_SUMMARY.utils.get_product_number import get_product_number
from T_NOVEL_SUMMARY.utils.process import process_date,process_number,parse_time,chinese_to_arabic, parse_date
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


class Xiang5Spider(scrapy.Spider):
    name = 'xiang5'
    allowed_domains = ['www.xiang5.com']
    start_urls = []
    lists = [
        'http://www.xiang5.com/bookinfo/24314.html'
    ]
    for l in lists:
        start_urls.append(l)

    def parse(self, response):
        print('1,=========================',response.url)
        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            # "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Cookie": "UM_distinctid=164daf563af44a-0b77993c46f21-6114147a-100200-164daf563b0422; canal=0; schannelm=0; www_say=775abff326250295f011c827045e4f45; PHPSESSID=imbduief49qgu8e9mttjtb03u1; Hm_lvt_688746b9e4f9d33e0e2ce6aeffb4fa58=1535520731,1535597551; counter=zixing; countertime=2018/8/30; _jzqc=1; _qzjc=1; CNZZDATA1253179669=891460335-1532681545-%7C1535606694; Hm_lpvt_688746b9e4f9d33e0e2ce6aeffb4fa58=1535610428; uuid=2AE001D147E7F1C7E3026160C9234536; marks=13; _qzja=1.754836888.1532681874609.1535597551629.1535610427783.1535602634139.1535610427783.0.0.0.22.6; _qzjto=18.2.0; _jzqa=1.4298357099084273000.1532681875.1535597552.1535610428.6; _jzqx=1.1535610428.1535610428.1.jzqsr=xiang5%2Ecom|jzqct=/.-; _jzqckmp=1; _jzqb=1.1.10.1535610428.1; _qzjb=1.1535610427783.1.0.0.0",
            "Host": "www.xiang5.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
        }
        if response.status != 200:
            yield scrapy.Request(url=response.url, headers=headers, callback=self.parse, dont_filter=True)
        else:
            print('请求成功>>>')
            item = TNovelSummaryItem()
            src_url = response.url
            item["src_url"] = src_url
            print('src_url:', src_url)
            product_number = ' '.join(response.xpath('//div[@class=" fr worksLR"]/h4/text()').extract()).strip()
            print('product_number:', product_number)
            product_number = get_product_number(product_number)
            print('product_number:', product_number)
            item["product_number"] = product_number
            plat_number = 'P35'
            print('plat_number:', plat_number)
            item["plat_number"] = plat_number
            Chapter_num_update = ''.join(response.xpath('//div[@class="worksL2"]/h2/b[@class="colR"]/a/text()').extract()).strip()
            Chapter_num_update = ''.join(re.findall(r'第(\d+)章',Chapter_num_update, re.I|re.M))
            item["Chapter_num_update"] = Chapter_num_update
            print('Chapter_num_update:',Chapter_num_update)
            update_date = ''.join(response.xpath('//div[@class="worksL2"]/h2/text()').extract()).strip()
            # print('update_date:', update_date)
            update_date = re.match(r'([\d+]{4}\-[\d+]{2}\-[\d+]{2}\s[\d+]{2}\:[\d+]{2}\:[\d+]{2})',update_date, re.I|re.S ).group()
            item["update_date"] = update_date
            print('update_date:',update_date)
            words = ''.join(response.xpath('//div[@class="workSecHit"]/span/text()').extract()).strip()
            words = ' '.join(re.findall(r'字数：(.*)', words, re.I|re.M))
            words = process_number(words)
            item["words"] = words
            print('words:',words)
            click_num = ''.join(response.xpath('//div[@class="workSecHit"]/span/text()').extract()).strip()
            click_num = ''.join(re.findall(r'点击：(\d+)\s', click_num, re.I|re.M))
            item["click_num"] = click_num
            print('click_num:',click_num)
            collect_num = ''.join(response.xpath('//div[@class="workSecHit"]/span/text()').extract()).strip()
            collect_num = ''.join(re.findall(r'收藏：(\d+)\s', collect_num, re.I|re.M))
            item["collect_num"] = collect_num
            print('collect_num:',collect_num)
            tickets_num = None
            item["tickets_num"] = tickets_num
            comment_num = ''.join(response.xpath('//*[@id="pinglun"]/h4/span[@class="fl"]/b/text()').extract()).strip()
            comment_num = ''.join(re.findall(r'(\d+)', comment_num, re.I|re.M))
            item["comment_num"] = comment_num
            print('comment_num:',comment_num)
            score = None
            item["score"] = score
            reward_num = None
            item["reward_num"] = reward_num
            last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["last_modify_date"] = last_modify_date
            print('last_modify_date:', last_modify_date)

            print(item)
            yield item

