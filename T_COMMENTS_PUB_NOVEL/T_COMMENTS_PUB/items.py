# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TCommentsPubItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_number = scrapy.Field()  # 产品编号
    plat_number = scrapy.Field()  # 平台编号
    nick_name = scrapy.Field()  # 用户名/昵称
    cmt_date = scrapy.Field()  # 评论日期
    cmt_time = scrapy.Field()  # 评论时间
    comments = scrapy.Field()  # 评论内容
    like_cnt = scrapy.Field()  # 评论点赞数(有用数)
    cmt_reply_cnt = scrapy.Field()  # 评论回复数
    long_comment = scrapy.Field()  # 长评论
    last_modify_date = scrapy.Field()  # 最后一次采集时间
    src_url = scrapy.Field()  # 采集链接

