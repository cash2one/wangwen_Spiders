# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TNovelSummaryItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_number = scrapy.Field()  # 产品编号
    plat_number = scrapy.Field()  # 平台编号
    Chapter_num_update = scrapy.Field()  # 更新章数
    update_date = scrapy.Field()  #更新日期
    words = scrapy.Field()  #字数
    click_num = scrapy.Field()  #总点击量
    tickets_num = scrapy.Field()  #月票量
    comment_num = scrapy.Field()  #评论总数
    score = scrapy.Field()  #评分
    collect_num = scrapy.Field()  #总收藏数
    reward_num = scrapy.Field()   #月打赏数
    last_modify_date = scrapy.Field()  #最后一次采集时间
    src_url = scrapy.Field()  #采集源链接
