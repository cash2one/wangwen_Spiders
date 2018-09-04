
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
    name = 'book_qq'
    allowed_domains = ['book.qq.com','dushu.qq.com']
    start_urls = []
    lists = [
        'http://book.qq.com/intro.html?bid=AGkENl1mVjEAPVRj&sword=扶摇皇后',
        'http://book.qq.com/intro.html?bid=AGoENl1pVjAAPlRm&sword=修罗武神',
        'http://book.qq.com/intro.html?bid=AG4EPV1mVjEAOlRg&sword=万古仙穹',
        'http://book.qq.com/intro.html?bid=AGAEMF1iVjYAOVRm&sword=人皇纪',
        'http://book.qq.com/intro.html?bid=AGAENV1oVjAAPFRk&sword=九星霸体诀',
        'http://book.qq.com/intro.html?bid=AGAENF1jVj4APVRg&sword=吞天记',
        'http://book.qq.com/intro.html?bid=AG4EMl1mVjEAM1Rt&sword=龙纹战神',
        'http://book.qq.com/intro.html?bid=AGAENl1pVjAAP1Rl&sword=英雄联盟之决胜巅峰',
        'http://book.qq.com/intro.html?bid=AGsEMl1kVj8AM1Rj&sword=我的26岁女房客',
        'http://book.qq.com/intro.html?bid=AGAENV1oVjAAMlRn&sword=八荒剑神',
        'http://book.qq.com/intro.html?bid=AGAEN11hVjIAOVRt&sword=女总裁的特种神医',
        'http://book.qq.com/intro.html?bid=AGEEN11mVjcAMlRs&sword=破天录',
        'http://book.qq.com/intro.html?bid=AGsEMV1kVjEAMlRn&sword=道神',
        'http://book.qq.com/intro.html?bid=AGwEN11mVjMAMlRm&sword=神医高手在都市',
        'http://book.qq.com/intro.html?bid=AGsEPF1lVjQAOVRs&sword=早安，老公大人',
        'http://book.qq.com/intro.html?bid=AGsEMl1lVj8APVRk&sword=近身兵王',
        'http://book.qq.com/intro.html?bid=AGAEN11jVjQAP1Ri&sword=超能神医',
        'http://book.qq.com/intro.html?bid=AGEENl1mVjEAO1Rg&sword=庶女惊华：一品毒医',
        'http://book.qq.com/intro.html?bid=AGoEM11nVjAAM1Rk&sword=雷武',
        'http://book.qq.com/intro.html?bid=AGAENF1mVjUAPFRh&sword=碎星物语',
        'http://book.qq.com/intro.html?bid=AGwENV1pVjIAPlRs&sword=神级插班生',
        'http://book.qq.com/intro.html?bid=AGwEMF1nVjAAOlRh&sword=神级高手在都市',
        'http://book.qq.com/intro.html?bid=AGEEN11jVjIAPFRh&sword=天行',
        'http://book.qq.com/intro.html?bid=AGAEMF1pVjEAOlRj&sword=锦堂归燕',
        'http://book.qq.com/intro.html?bid=AGEENV1gVjMAP1Rt&sword=凌霄之上',
        'http://book.qq.com/intro.html?bid=AGAENF1nVjQAMlRj&sword=超级鉴宝师',
        'http://book.qq.com/intro.html?bid=AG4EPF1kVjQAPVRm&sword=命之途',
        'http://book.qq.com/intro.html?bid=AGAENF1mVj8APVRi&sword=乱唐',
        'http://book.qq.com/intro.html?bid=AGAEMV1jVjIAO1Rk&sword=巫师纪元',
        'http://book.qq.com/intro.html?bid=AGkEPF1jVjQAO1Rj&sword=龙血战神',
        'http://book.qq.com/intro.html?bid=AGkEM11iVjcAPVRn&sword=武逆',
        'http://book.qq.com/intro.html?bid=AGkEMV1kVjcAPFRg&sword=混沌剑神',
        'http://book.qq.com/intro.html?bid=AGkEN11kVjEAO1Rn&sword=不灭武尊',
        'http://book.qq.com/intro.html?bid=AGkEM11iVjYAOlRk&sword=武道至尊',
        'http://book.qq.com/intro.html?bid=AGAENl1gVjYAPVRj&sword=龙符',
        'http://book.qq.com/intro.html?bid=AGAEMF1oVjUAOFRt&sword=大逆之门',
        'http://book.qq.com/intro.html?bid=AGAEN11nVjQAPlRj&sword=万域之王',
        'http://book.qq.com/intro.html?bid=AGEENF1oVjcAPFRs&sword=最强逆袭',
        'http://book.qq.com/intro.html?bid=AGAEMV1oVjQAPlRi&sword=医品宗师',
        'http://book.qq.com/intro.html?bid=AGEEN11kVj4APlRs&sword=圣武星辰',
        'http://book.qq.com/intro.html?bid=AGAEMV1hVjcAO1Rl&sword=祭炼山河',
        'http://book.qq.com/intro.html?bid=AG8ENl1gVjUAOFRi&sword=御天神帝',
        'http://book.qq.com/intro.html?bid=AGAEMF1pVjQAPVRj&sword=火帝神尊',
        'http://book.qq.com/intro.html?bid=AG0EMl1hVj8APlRk&sword=永夜君王',
        'http://book.qq.com/intro.html?bid=AGAEN11pVj8APVRg&sword=锦衣春秋',
        'http://book.qq.com/intro.html?bid=AG8ENF1nVjMAP1Rs&sword=剑王朝',
        'http://book.qq.com/intro.html?bid=AG0EMl1hVj8AO1Ri&sword=逆天邪神',
        'http://book.qq.com/intro.html?bid=AG8EPV1oVj4AM1Rh&sword=纯禽记者',
        'http://book.qq.com/intro.html?bid=AGkEM11pVjEAP1Rj&sword=圣王',
        'http://book.qq.com/intro.html?bid=AGAEN11gVjUAPlRg&sword=逆鳞',
        'http://book.qq.com/intro.html?bid=AGAENF1jVjEAM1Rl&sword=大夏王侯',
        'http://book.qq.com/intro.html?bid=AGkEM11iVj8APFRh&sword=雪中悍刀行',
        'http://book.qq.com/intro.html?bid=AGAENF1jVj4APVRn&sword=无敌剑域',
        'http://book.qq.com/intro.html?bid=AG8EN11jVjMAMlRl&sword=盖世帝尊',
        'http://book.qq.com/intro.html?bid=AGoEN11mVj8AMlRi&sword=星河大帝',
        'http://book.qq.com/intro.html?bid=AG0EN11mVjYAMlRk&sword=极品透视',
        'http://book.qq.com/intro.html?bid=AGsENF1oVjEAMlRm&sword=不败战神',
        'http://book.qq.com/intro.html?bid=AG0ENl1hVjQAOFRm&sword=混世刁民',
        'http://book.qq.com/intro.html?bid=AGsENF1oVjEAPVRs&sword=仙路争锋',
        'http://book.qq.com/intro.html?bid=AG4ENl1mVjMAOlRh&sword=终极教师',
        'http://book.qq.com/intro.html?bid=AGAENF1jVj4APFRj&sword=十方神王',
        'http://book.qq.com/intro.html?bid=AGsENF1nVjcAO1Rn&sword=冰火破坏神',
        'http://book.qq.com/intro.html?bid=AGEENV1gVj4APlRk&sword=在七扇门当差的日子',
        'http://book.qq.com/intro.html?bid=AG8EPV1hVjUAPFRi&sword=陆少的暖婚新妻',
        'http://book.qq.com/intro.html?bid=AGAEMF1nVj4APFRh&sword=魔域',
        'http://book.qq.com/intro.html?bid=AGAEMV1iVjMAPVRj&sword=唐谋天下',
        'http://book.qq.com/intro.html?bid=AGoEN11pVjQAO1Rh&sword=刀剑神皇',
        'http://book.qq.com/intro.html?bid=AG4EN11jVjQAPFRm&sword=仙路至尊',
        'http://book.qq.com/intro.html?bid=AGkEM11kVjIAPlRk&sword=问镜',
        'http://book.qq.com/intro.html?bid=AGAEMF1oVjUAOVRk&sword=儒武争锋',
        'http://book.qq.com/intro.html?bid=AGEEN11lVjIAMlRk&sword=绝命毒尸',
        'http://book.qq.com/intro.html?bid=AGkEPF1kVjYAP1Rn&sword=国色生枭',
        'http://book.qq.com/intro.html?bid=AG4EN11kVjEAPlRh&sword=戮仙',
        'http://dushu.qq.com/intro.html?bid=914788&sword=一寸相思',
        'http://dushu.qq.com/intro.html?bid=164524&sword=微微一笑很倾城',
        'http://dushu.qq.com/intro.html?bid=243573&sword=骄阳似我（上）',
        'http://dushu.qq.com/intro.html?bid=457353&sword=不负如来不负卿',
        'http://dushu.qq.com/intro.html?bid=837818&sword=南方有乔木',
        'http://dushu.qq.com/intro.html?bid=144509&sword=杉杉来吃',
        'http://dushu.qq.com/intro.html?bid=854572&sword=散落星河的记忆',
        'http://dushu.qq.com/intro.html?bid=920794&sword=蜜汁炖鱿鱼',
        'http://book.qq.com/intro.html?bid=AGAENF1jVj4APVRm&sword=绝世邪神',
        'http://book.qq.com/intro.html?bid=AG4EM11jVjEAO1Rl&sword=神医嫡女',
        'http://book.qq.com/intro.html?bid=AG8EN11lVj4AP1Rh&sword=第七任新娘',
        'http://book.qq.com/intro.html?bid=AG4EMl1jVj4APVRs&sword=倾国太后',

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
        product_number = ''.join(response.xpath('//h3/a/text()').extract()).strip()
        print('product_number:', product_number)
        product_number = get_product_number(product_number)
        print('product_number:', product_number)
        item["product_number"] = product_number
        plat_number = 'P17'
        print('plat_number:', plat_number)
        item["plat_number"] = plat_number
        Chapter_num_update = ''.join(response.xpath('//div[@class="new_list"]/dl[1]/dd[1]/a/text()').extract()).strip()
        if Chapter_num_update:
            Chapter_num_update = ''.join(re.findall(r'第(\d+)章',Chapter_num_update, re.I|re.M))
            item["Chapter_num_update"] = Chapter_num_update
            print('Chapter_num_update:',Chapter_num_update)
        else:
            Chapter_num_update = None
            item["Chapter_num_update"] = Chapter_num_update
            print('Chapter_num_update:', Chapter_num_update)
        update_date = ''.join(response.xpath('//div[@class="new_list"]/dl[1]/dd[@class="gray"]/text()').extract()).strip()
        if update_date:
            item["update_date"] = update_date
            print('update_date:',update_date)
        else:
            update_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item["update_date"] = update_date
            print('update_date:', update_date)
        words = ''.join(response.xpath('//div[@id="bookinfo"]/div[@class="book_info"]/dl[1]/dd[last()]/text()').extract()).strip()
        if '字' in words:
            words = words.replace('字','')
            words = process_number(words)
            item["words"] = words
            print('words:',words)
        else:
            words = process_number(words)
            item["words"] = words
            print('words:', words)
        click_num = None
        item["click_num"] = click_num
        tickets_num = None
        item["tickets_num"] = tickets_num
        comment_num = ''.join(response.xpath('//*[@id="commentCount"]/text()').extract()).strip()
        item["comment_num"] = comment_num
        print('comment_num:',comment_num)
        score = ''.join(response.xpath('//*[@id="StarIco"]/span[@id="StarIcoValue"]/b//text()').extract()).strip()
        item["score"] = score
        print('score:',score)
        collect_num = None
        item["collect_num"] = collect_num
        reward_num = None
        item["reward_num"] = reward_num
        last_modify_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item["last_modify_date"] = last_modify_date
        print('last_modify_date:', last_modify_date)
        yield item
