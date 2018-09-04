# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TNovelItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_number = scrapy.Field()  #产品编号
    plat_number = scrapy.Field()  #平台编号
    author = scrapy.Field()   #作者
    novel_type = scrapy.Field()  #分类
    tags = scrapy.Field()  #标签
    Signed = scrapy.Field()  #签约
    novel_desc = scrapy.Field() #简介
    Product_image = scrapy.Field()  #产品图片
    last_modify_date = scrapy.Field()  #最后一次采集时间
    src_url = scrapy.Field() #采集源链接
