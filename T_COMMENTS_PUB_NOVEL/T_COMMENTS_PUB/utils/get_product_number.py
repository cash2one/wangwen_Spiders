# -*- coding: utf-8 -*-
from T_COMMENTS_PUB.utils.Mydb import Mydb

mydb = Mydb('127.0.0.1','root','root','wenchan',charset='utf8')


def get_product_number(value):
    sql = 'select * from T_PRODUCT where product_type="E" and product_name="{}"'.format(value)
    res = mydb.query(sql)
    # print(len(res))
    for r in res:
        R1 = r[1]
        R0 = r[0]
        if R1 in value:
            product_number_info = R0
            # print('product_number_info:',product_number_info)
            return product_number_info

# get_product_number('天官赐福')
# get_product_number('【综】炮灰专业户')

def get_product_statistical(value):
    sql = 'select product_number,plat_number, comments from t_comments_pub_qingxi where comments like "%{}%"'.format(value)
    sql_1 = 'select product_number,plat_number,count(*)  from t_comments_pub_qingxi where comments like "%{}%" GROUP by plat_number'.format(value)
    sql_2 = 'select id from t_comments_pub where comments like "%{}%"'.format(value)
    sql_3 = 'DELETE FROM t_comments_pub where id in (select id from (select id from t_comments_pub  where comments like "%{}%") as b)'.format(value)
    sql_4 = 'DELETE FROM t_comments_pub_qingxi where comments like "%{}%"'.format(value)
    sql_5 = 'select n.product_name,p.plat_name,m.comments,m.cmt_date,m.cmt_reply_cnt,m.src_url from t_comments_pub m,t_product n ,t_plat p   where  m.product_number=n.product_number and m.plat_number=p.plat_number and n.product_name="{}"'.format(value)
    #
    res = mydb.query(sql)
    print(len(res))
    for r in res:
        print(r)

    # dels = mydb.exe(sql_4)
    # print(dels)

# get_product_statistical('支持一下')
# get_product_statistical('大神红票榜上升3名 ')
# get_product_statistical('赏红包')
# get_product_statistical('良辰看好你的文，一片丹青照我心！')
# get_product_statistical('这本书太好看了！9000红薯币红包送上，希望后续更加精彩！')
# get_product_statistical('红票')

# get_product_statistical('有人节操好，有人人品好，有人智商好……但是……我心情好，砸你个地雷，不要潜水了出来码字吧~~~')


