# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql.cursors
# from scrapy import log
from twisted.enterprise import adbapi
from T_NOVEL_SUMMARY.utils.Mydb import Mydb
import json



class TNovelSummaryPipeline(object):
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
        # select_sql = "select * from t_novel_summary where product_number='{}'and update_date='{}'".format(
        #     item["product_number"], item["update_date"])
        # mydb = Mydb('127.0.0.1', 'root', 'root', 'wenchan', charset='utf8')
        # data = mydb.query(select_sql)
        # if data:
        #     print('>>>该条数据已重复>>>')
        #     return False
        # else:
        
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
            insert into T_NOVEL_SUMMARY(product_number,plat_number,Chapter_num_update,update_date,words,click_num,tickets_num,comment_num,score,collect_num,reward_num,last_modify_date,src_url)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)on duplicate key update product_number = values(product_number),plat_number = VALUES (plat_number),Chapter_num_update = VALUES (Chapter_num_update),update_date=VALUES (update_date),words=VALUES (words),click_num=VALUES (click_num),tickets_num=VALUES (tickets_num),comment_num=VALUES (comment_num),score=VALUES (score),collect_num=VALUES (collect_num),reward_num=VALUES (reward_num),last_modify_date=VALUES (last_modify_date),src_url=VALUES (src_url)
            """

        try:
            cursor.execute(insert_sql, (
             item["product_number"], item["plat_number"], item["Chapter_num_update"], item["update_date"],
            item["words"], item["click_num"], item["tickets_num"], item["comment_num"],item["score"],item["collect_num"],item["reward_num"],
            item["last_modify_date"],item["src_url"]))
            print('插入数据库成功>>>')
        except Exception as e:
            print("执行sql语句>插入数据失败：%s" % (str(e)),item)