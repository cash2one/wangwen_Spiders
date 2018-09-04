# -*- coding: utf-8 -*-
from T_NOVEL_SUMMARY.utils.Mydb import Mydb

mydb = Mydb('127.0.0.1','root','root','wenchan',charset='utf8')

def get_product_number(value):
    sql = 'select * from T_PRODUCT WHERE product_type="E" and product_name="{}"'.format(value)
    res = mydb.query(sql)
    # print(len(res))
    for r in res:
        # print(r)
        R1 = r[1]
        R0 = r[0]
        if R1 in value:
            product_number_info = R0
            # print('product_number_info:',product_number_info)
            return product_number_info

# get_product_number('杉杉来吃（赵丽颖、张翰主演）')
# get_product_number('【综】炮灰专业户')