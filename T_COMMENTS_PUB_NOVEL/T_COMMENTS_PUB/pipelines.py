# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html



import pymysql.cursors
# from scrapy import log
import logging
import json
from twisted.enterprise import adbapi
from scrapy.exceptions import DropItem
from T_COMMENTS_PUB.items import TCommentsPubItem
from T_COMMENTS_PUB.utils.Mydb import Mydb


class TCommentsPubPipeline(object):
    def process_item(self, item, spider):
        return item



#以json格式保存
class DataPipeline(object):
    def __init__(self):
        self.f = open('position.json','w',encoding='utf-8')

    def process_item(self,item,spider):
        self.f.write(json.dumps(dict(item),ensure_ascii=False) + '\n')
        return item

    def close_spider(self,spider):
        self.f.close()


#存入mysql数据库
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # 需要在setting中设置数据库配置参数
        dbparms = dict(
            host=settings['MYSQL_HOST'],
            port=settings['MYSQL_PORT'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor,
            use_unicode=True,
        )
        # 连接ConnectionPool（使用MySQLdb连接，或者pymysql）
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)  # **让参数变成可变化参数
        return cls(dbpool)   # 返回实例化对象


    def process_item(self, item, spider):
        select_sql = "select * from T_COMMENTS_PUB where nick_name='{}'and cmt_time='{}' and comments='{}'".format(item["nick_name"], item["cmt_time"], item["comments"])
        mydb = Mydb('127.0.0.1', 'root', 'root', 'wenchan', charset='utf8')
        data = mydb.query(select_sql)
        if data:
            print('>>>该条数据已重复>>>')
            return False
        else:
            # 使用twisted将MySQL插入变成异步执行
            query = self.dbpool.runInteraction(self.do_insert, item)
            # 添加异常处理
            query.addCallback(self.handle_error)


    def handle_error(self, failure):
        # 处理异步插入时的异常
        print(failure)


    def do_insert(self, cursor, item):
        # 执行具体的插入
        insert_sql = """
            insert into T_COMMENTS_PUB(product_number,plat_number,nick_name,cmt_date,cmt_time,comments,like_cnt,cmt_reply_cnt,long_comment,last_modify_date,src_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

        try:
            cursor.execute(insert_sql, (item["product_number"],item["plat_number"],item["nick_name"],item["cmt_date"],item["cmt_time"],item["comments"],item["like_cnt"],item["cmt_reply_cnt"],item["long_comment"],item["last_modify_date"],item["src_url"]))
            print('插入数据库成功>>>')
        except Exception as e:
            print("执行sql语句失败：%s" % (str(e)),item)


