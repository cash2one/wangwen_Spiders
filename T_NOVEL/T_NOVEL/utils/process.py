# -*- coding: utf-8 -*-
import time
import re
import datetime
from datetime import timedelta

num_pattern = re.compile(r'\d+')
num_pt = re.compile(r'[\d+]-[\d+]')

def parse_time(date):
    if re.match('刚刚', date):
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    if re.match('\d+分钟前', date):
        minute = re.match('(\d+)', date).group(1)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - float(minute) * 60))
    if re.match('\d+小时前', date):
        hour = re.match('(\d+)', date).group(1)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - float(hour) * 60 * 60))
    # if re.match('昨天.*', date):
    #     date = re.match('昨天(.*)', date).group(1).strip()
    #     date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime() - 24 * 60 * 60) + ' ' + date
    if "昨天" in date:
        date = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
    if re.match('\d+天前',date):
        day = re.match('(\d+)', date).group(1)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - float(day) * 24 * 60 * 60))
    if re.match('\d+周前',date):
        week = re.match('(\d+)', date).group(1)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - float(week) * 7 * 24 * 60 * 60))
    if re.match('\d+个月前',date):
        month = re.match('(\d+)', date).group(1)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - float(month) * 30.46 * 24 * 60 * 60))
    if re.match('\d+年前',date):
        year = re.match('(\d+)', date).group(1)
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() - float(year) * 12 * 30.445 * 24 * 60 * 60))
        print('date:',date)
    if re.match('\d{2}-\d{2}', date):
        date = time.strftime('%Y-', time.localtime()) + date + ' 00:00:00'
    # if re.match('\d{4}-\d{2}-\d{2}', date):
    #     date = date + ' ' +datetime.datetime.now().strftime('%H:%M:%S')
    # print(date)
    return date

def parse_date(value):
    if '今天' in value:
        times = re.match(r'今天  ([\d+]{2}\:[\d+]{2})',value, re.I|re.M).group(1)
        print('times:',times)
        data = datetime.datetime.now().strftime('%Y-%m-%d ') + times
        print('data:',data)
    if '昨天' in value:
        times = re.match(r'昨天  ([\d+]{2}\:[\d+]{2})',value, re.I|re.M).group(1)
        print('times:', times)
        data = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d ') + times
        print('data:', data)
    if re.match('(\d+)月(\d+)日  (\d+\:\d+)', value):
        month = re.match('(\d+)月(\d+)日  (\d+\:\d+)', value).group(1)
        if len(month) < 2:
            month = '0' + month
            print('month:', month)
        else:
            month = month
            print('month:', month)
        day = re.match('(\d+)月(\d+)日  (\d+\:\d+)', value).group(2)
        if len(day) < 2:
            day = '0' + day
            print('day:', day)
        else:
            day = day
            print('day:', day)
        times = re.match('(\d+)月(\d+)日  (\d+\:\d+)', value).group(3)
        print('times:', times)
        data = time.strftime('%Y-', time.localtime()) + month + '-' + day + ' ' + times
        print('data:', data)
    else:
        data = None
        print('时间获取错误！！！')
    return data


def process_date(value):
    if '分钟前' in value:
        res = num_pattern.search(value).group()
        date = (datetime.datetime.now() - timedelta(days=int(res))).strftime('%Y-%m-%d')
    elif '小时前' in value:
        res = num_pattern.search(value).group()
        date = (datetime.datetime.now() - timedelta(days=int(res))).strftime('%Y-%m-%d')
    elif '天前' in value:
        res = num_pattern.search(value).group()
        date = (datetime.datetime.now() - timedelta(days=int(res))).strftime('%Y-%m-%d')
    elif "昨日" in value:
        date = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    # elif num_pt in value:
    #     date_pub = (datetime.datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    else:
        date = datetime.datetime.now().strftime('%Y-%m-%d')
    return date


def process_number(value):
    if '万' in value:
        res = value.replace('万','')
        number = float(res)*10000
        number = int(number)
        # print('number:',number)
    elif 'w+' in value:
        res = value.replace('w+','')
        number = float(res)*10000
        number = int(number)
        # print('number:',number)
    elif '亿' in value:
        res = value.replace('亿','')
        number = float(res)*100000000
        number = int(number)
        # print('number:',number)
    else:
        res = num_pattern.search(value).group()
        number = res
    return number

#中文数字转换成阿拉伯数字
common_used_numerals_tmp ={'零':0, '一':1, '二':2, '两':2, '三':3, '四':4, '五':5, '六':6, '七':7, '八':8, '九':9, '十':10, '百':100, '千':1000, '万':10000, '亿':100000000}
# common_used_numerals= dict(zip(common_used_numerals_tmp.values(), common_used_numerals_tmp.keys())) #反转
# print(common_used_numerals)
def chinesedigits(uchars_chinese):
      total = 0
      r = 1              #表示单位：个十百千...
      for i in range(len(uchars_chinese) - 1, -1, -1):
        # print(uchars_chinese[i])
        val = common_used_numerals_tmp.get(uchars_chinese[i])
        if val >= 10 and i == 0:  #应对 十三 十四 十*之类
          if val > r:
            r = val
            total = total + val
          else:
            r = r * val
            #total =total + r * x
        elif val >= 10:
          if val > r:
            r = val
          else:
            r = r * val
        else:
          total = total + r * val
      return total



#中文数字转换成阿拉伯数字
CN_NUM = {
    '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
    '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
}

CN_UNIT = {
    '十': 10,
    '拾': 10,
    '百': 100,
    '佰': 100,
    '千': 1000,
    '仟': 1000,
    '万': 10000,
    '萬': 10000,
    '亿': 100000000,
    '億': 100000000,
    '兆': 1000000000000,
}

def chinese_to_arabic(cn: str) -> int:
    unit = 0  # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val


def product_number(value):
    if '焚天之怒' in value:
        p_number = 'E0000001'
    elif '校花之贴身高手' in value:
        p_number = 'E0000002'
    elif '奶爸的文艺人生' in value:
        p_number = 'E0000003'
    elif '联盟之谁与争锋' in value:
        p_number = 'E0000004'
    elif '战神无敌' in value:
        p_number = 'E0000005'
    elif '凡人修仙传 ' in value:
        p_number = 'E0000006'
    elif '全职高手' in value:
        p_number = 'E0000007'
    elif '遮天' in value:
        p_number = 'E0000008'
    elif '异常生物见闻录' in value:
        p_number = 'E0000009'
    elif '逍遥小书生' in value:
        p_number = 'E0000010'
    elif '重生之财源滚滚' in value:
        p_number = 'E0000011'
    elif '最强兵王' in value:
        p_number = 'E0000012'
    elif '武动乾坤' in value:
        p_number = 'E0000013'
    elif '莽荒纪' in value:
        p_number = 'E0000014'
    elif '完美世界' in value:
        p_number = 'E0000015'
    elif '大主宰' in value:
        p_number = 'E0000016'
    elif '万界天尊' in value:
        p_number = 'E0000017'
    elif '唐砖' in value:
        p_number = 'E0000018'
    elif '余罪' in value:
        p_number = 'E0000019'
    elif '将夜' in value:
        p_number = 'E0000020'
    elif '最强弃少 ' in value:
        p_number = 'E0000021'
    elif '穿越火线之AK传奇' in value:
        p_number = 'E0000022'
    elif '' in value:
        p_number = 'E0000023'
    elif '' in value:
        p_number = 'E0000024'
    elif '' in value:
        p_number = 'E0000025'
    elif '' in value:
        p_number = 'E0000026'
    elif '' in value:
        p_number = 'E0000027'
    elif '' in value:
        p_number = 'E0000028'
    elif '' in value:
        p_number = 'E0000028'
    elif '' in value:
        p_number = 'E0000029'
    elif '' in value:
        p_number = 'E0000030'
    elif '' in value:
        p_number = 'E0000031'
    elif '' in value:
        p_number = 'E0000032'
    elif '' in value:
        p_number = 'E0000033'
    elif '' in value:
        p_number = 'E0000034'
    elif '' in value:
        p_number = 'E0000035'
    elif '' in value:
        p_number = 'E0000036'
    elif '' in value:
        p_number = 'E0000037'
    elif '' in value:
        p_number = 'E0000038'
    elif '' in value:
        p_number = 'E0000039'
    elif '' in value:
        p_number = 'E0000040'
    elif '' in value:
        p_number = 'E0000041'
    elif '' in value:
        p_number = 'E0000042'
    elif '' in value:
        p_number = 'E0000043'
    elif '' in value:
        p_number = 'E0000044'
    elif '' in value:
        p_number = 'E0000045'
    elif '' in value:
        p_number = 'E0000046'
    elif '' in value:
        p_number = 'E0000047'
    elif '' in value:
        p_number = 'E0000048'
    elif '' in value:
        p_number = 'E0000049'
    elif '' in value:
        p_number = 'E0000050'
    elif '' in value:
        p_number = 'E0000051'
    elif '' in value:
        p_number = 'E0000052'
    elif '' in value:
        p_number = 'E0000053'
    elif '' in value:
        p_number = 'E0000054'
    elif '' in value:
        p_number = 'E0000055'
    elif '' in value:
        p_number = 'E0000056'
    elif '' in value:
        p_number = 'E0000057'
    elif '' in value:
        p_number = 'E0000058'
    elif '' in value:
        p_number = 'E0000059'
    elif '' in value:
        p_number = 'E0000060'
    elif '' in value:
        p_number = 'E0000061'
    elif '' in value:
        p_number = 'E0000062'
    elif '' in value:
        p_number = 'E0000063'
    elif '' in value:
        p_number = 'E0000064'
    elif '' in value:
        p_number = 'E0000065'
    elif '' in value:
        p_number = 'E0000066'
    elif '' in value:
        p_number = 'E0000067'
    elif '' in value:
        p_number = 'E0000068'
    elif '' in value:
        p_number = 'E0000069'
    elif '' in value:
        p_number = 'E0000070'
    elif '' in value:
        p_number = 'E0000071'
    elif '' in value:
        p_number = 'E0000072'
    elif '' in value:
        p_number = 'E0000073'
    elif '' in value:
        p_number = 'E0000074'
    elif '' in value:
        p_number = 'E0000075'
    elif '' in value:
        p_number = 'E0000076'
    elif '' in value:
        p_number = 'E0000077'
    elif '' in value:
        p_number = 'E0000078'
    elif '' in value:
        p_number = 'E0000079'
    elif '' in value:
        p_number = 'E0000080'
    elif '' in value:
        p_number = 'E0000081'
    elif '' in value:
        p_number = 'E0000082'
    elif '' in value:
        p_number = 'E0000083'
    elif '' in value:
        p_number = 'E0000084'
    elif '' in value:
        p_number = 'E0000085'
    elif '' in value:
        p_number = 'E0000086'
    elif '' in value:
        p_number = 'E0000087'
    elif '' in value:
        p_number = 'E0000088'
    elif '' in value:
        p_number = 'E0000089'
    elif '' in value:
        p_number = 'E0000090'
    elif '' in value:
        p_number = 'E0000091'
    elif '' in value:
        p_number = 'E0000092'
    elif '' in value:
        p_number = 'E0000093'
    elif '' in value:
        p_number = 'E0000094'
    elif '' in value:
        p_number = 'E0000095'
    elif '' in value:
        p_number = 'E0000096'
    elif '' in value:
        p_number = 'E0000097'
    elif '' in value:
        p_number = 'E0000098'
    elif '' in value:
        p_number = 'E0000099'
    elif '' in value:
        p_number = 'E0000100'
    elif '' in value:
        p_number = 'E0000101'
    elif '' in value:
        p_number = 'E0000102'
    elif '' in value:
        p_number = 'E0000103'
    elif '' in value:
        p_number = 'E0000104'
    elif '' in value:
        p_number = 'E0000105'
    elif '' in value:
        p_number = 'E0000106'
    elif '' in value:
        p_number = 'E0000107'
    elif '' in value:
        p_number = 'E0000108'
    elif '' in value:
        p_number = 'E0000109'
    elif '' in value:
        p_number = 'E0000110'
    elif '' in value:
        p_number = 'E0000111'
    elif '' in value:
        p_number = 'E0000112'
    elif '' in value:
        p_number = 'E0000113'
    elif '' in value:
        p_number = 'E0000114'
    elif '' in value:
        p_number = 'E0000115'
    elif '' in value:
        p_number = 'E0000116'
    elif '' in value:
        p_number = 'E0000117'
    elif '' in value:
        p_number = 'E0000118'
    elif '' in value:
        p_number = 'E0000119'
    elif '' in value:
        p_number = 'E0000120'
    elif '' in value:
        p_number = 'E0000121'
    elif '' in value:
        p_number = 'E0000122'
    elif '' in value:
        p_number = 'E0000123'
    elif '' in value:
        p_number = 'E0000124'
    elif '' in value:
        p_number = 'E0000125'
    elif '' in value:
        p_number = 'E0000126'
    elif '' in value:
        p_number = 'E0000127'
    elif '' in value:
        p_number = 'E0000128'
    elif '' in value:
        p_number = 'E0000129'
    elif '' in value:
        p_number = 'E0000130'
    elif '' in value:
        p_number = 'E0000131'
    elif '' in value:
        p_number = 'E0000132'
    elif '' in value:
        p_number = 'E0000133'
    elif '' in value:
        p_number = 'E0000134'
    elif '' in value:
        p_number = 'E0000135'
    elif '' in value:
        p_number = 'E0000136'
    elif '' in value:
        p_number = 'E0000137'
    elif '' in value:
        p_number = 'E0000138'
    elif '' in value:
        p_number = 'E0000139'
    elif '' in value:
        p_number = 'E0000140'
    elif '' in value:
        p_number = 'E0000141'
    elif '' in value:
        p_number = 'E0000142'
    elif '' in value:
        p_number = 'E0000143'
    elif '' in value:
        p_number = 'E0000144'
    elif '' in value:
        p_number = 'E0000145'
    elif '' in value:
        p_number = 'E0000146'
    elif '' in value:
        p_number = 'E0000147'
    elif '' in value:
        p_number = 'E0000148'
    elif '' in value:
        p_number = 'E0000149'
    elif '' in value:
        p_number = 'E0000150'
    elif '' in value:
        p_number = 'E0000151'
    elif '' in value:
        p_number = 'E0000152'
    elif '' in value:
        p_number = 'E0000153'
    elif '' in value:
        p_number = 'E0000154'
    elif '' in value:
        p_number = 'E0000155'
    elif '' in value:
        p_number = 'E0000156'
    elif '' in value:
        p_number = 'E0000157'
    elif '' in value:
        p_number = 'E0000158'
    elif '' in value:
        p_number = 'E0000159'
    elif '' in value:
        p_number = 'E0000160'
    elif '' in value:
        p_number = 'E0000161'
    elif '' in value:
        p_number = 'E0000162'
    elif '' in value:
        p_number = 'E0000163'
    elif '' in value:
        p_number = 'E0000164'
    elif '' in value:
        p_number = 'E0000165'
    elif '' in value:
        p_number = 'E0000166'
    elif '' in value:
        p_number = 'E0000167'
    elif '' in value:
        p_number = 'E0000168'
    elif '' in value:
        p_number = 'E0000169'
    elif '' in value:
        p_number = 'E0000170'
    elif '' in value:
        p_number = 'E0000171'
    elif '' in value:
        p_number = 'E0000172'
    elif '' in value:
        p_number = 'E0000173'
    elif '' in value:
        p_number = 'E0000174'
    elif '' in value:
        p_number = 'E0000175'
    elif '' in value:
        p_number = 'E0000176'
    elif '' in value:
        p_number = 'E0000177'
    elif '' in value:
        p_number = 'E0000178'
    elif '' in value:
        p_number = 'E0000179'
    elif '' in value:
        p_number = 'E0000180'
    elif '' in value:
        p_number = 'E0000181'
    elif '' in value:
        p_number = 'E0000182'
    elif '' in value:
        p_number = 'E0000183'
    elif '' in value:
        p_number = 'E0000184'
    elif '' in value:
        p_number = 'E0000185'
    elif '' in value:
        p_number = 'E0000186'
    elif '' in value:
        p_number = 'E0000187'
    elif '' in value:
        p_number = 'E0000188'
    elif '' in value:
        p_number = 'E0000189'
    elif '' in value:
        p_number = 'E0000190'
    elif '' in value:
        p_number = 'E0000191'
    elif '' in value:
        p_number = 'E0000192'
    elif '' in value:
        p_number = 'E0000193'
    elif '' in value:
        p_number = 'E0000194'
    elif '' in value:
        p_number = 'E0000195'
    elif '' in value:
        p_number = 'E0000196'
    elif '' in value:
        p_number = 'E0000197'
    elif '' in value:
        p_number = 'E0000198'
    elif '' in value:
        p_number = 'E0000199'
    elif '' in value:
        p_number = 'E0000200'
    elif '' in value:
        p_number = 'E0000201'
    elif '' in value:
        p_number = 'E0000202'
    elif '' in value:
        p_number = 'E0000203'
    elif '' in value:
        p_number = 'E0000204'
    elif '' in value:
        p_number = 'E0000205'
    elif '' in value:
        p_number = 'E0000206'
    elif '' in value:
        p_number = 'E0000207'
    elif '' in value:
        p_number = 'E0000208'
    elif '' in value:
        p_number = 'E0000209'
    elif '' in value:
        p_number = 'E0000210'
    elif '' in value:
        p_number = 'E0000211'
    elif '' in value:
        p_number = 'E0000212'
    elif '' in value:
        p_number = 'E0000213'
    elif '' in value:
        p_number = 'E0000214'
    elif '' in value:
        p_number = 'E0000215'
    elif '' in value:
        p_number = 'E0000216'
    elif '' in value:
        p_number = 'E0000217'
    elif '' in value:
        p_number = 'E0000218'
    elif '' in value:
        p_number = 'E0000219'
    elif '' in value:
        p_number = 'E0000220'
    elif '' in value:
        p_number = 'E0000221'
    elif '' in value:
        p_number = 'E0000222'
    elif '' in value:
        p_number = 'E0000223'
    elif '' in value:
        p_number = 'E0000224'
    elif '' in value:
        p_number = 'E0000225'
    elif '' in value:
        p_number = 'E0000226'
    elif '' in value:
        p_number = 'E0000227'
    elif '' in value:
        p_number = 'E0000228'
    elif '' in value:
        p_number = 'E0000229'
    elif '' in value:
        p_number = 'E0000230'
    elif '' in value:
        p_number = 'E0000231'
    elif '' in value:
        p_number = 'E0000232'
    elif '' in value:
        p_number = 'E0000233'
    elif '' in value:
        p_number = 'E0000234'
    elif '' in value:
        p_number = 'E0000235'
    elif '' in value:
        p_number = 'E0000236'
    elif '' in value:
        p_number = 'E0000237'
    elif '' in value:
        p_number = 'E0000238'
    elif '' in value:
        p_number = 'E0000239'
    elif '' in value:
        p_number = 'E0000240'
    elif '' in value:
        p_number = 'E0000241'
    elif '' in value:
        p_number = 'E0000242'
    elif '' in value:
        p_number = 'E0000243'
    elif '' in value:
        p_number = 'E0000244'
    elif '' in value:
        p_number = 'E0000245'
    elif '' in value:
        p_number = 'E0000246'
    elif '' in value:
        p_number = 'E0000247'
    elif '' in value:
        p_number = 'E0000248'
    elif '' in value:
        p_number = 'E0000249'
    elif '' in value:
        p_number = 'E0000250'
    elif '' in value:
        p_number = 'E0000251'
    elif '' in value:
        p_number = 'E0000252'
    elif '' in value:
        p_number = 'E0000253'
    elif '' in value:
        p_number = 'E0000254'
    elif '' in value:
        p_number = 'E0000255'
    elif '' in value:
        p_number = 'E0000256'
    elif '' in value:
        p_number = 'E0000257'
    elif '' in value:
        p_number = 'E0000258'
    elif '' in value:
        p_number = 'E0000259'
    elif '' in value:
        p_number = 'E0000260'
    elif '' in value:
        p_number = 'E0000261'
    elif '' in value:
        p_number = 'E0000262'
    elif '' in value:
        p_number = 'E0000263'
    elif '' in value:
        p_number = 'E0000264'
    elif '' in value:
        p_number = 'E0000265'
    elif '' in value:
        p_number = 'E0000266'
    elif '' in value:
        p_number = 'E0000267'
    elif '' in value:
        p_number = 'E0000268'
    elif '' in value:
        p_number = 'E0000269'
    elif '' in value:
        p_number = 'E0000270'
    elif '' in value:
        p_number = 'E0000271'
    elif '' in value:
        p_number = 'E0000272'
    elif '' in value:
        p_number = 'E0000273'
    elif '' in value:
        p_number = 'E0000274'
    elif '' in value:
        p_number = 'E0000275'
    elif '' in value:
        p_number = 'E0000276'
    elif '' in value:
        p_number = 'E0000277'
    elif '' in value:
        p_number = 'E0000278'
    elif '' in value:
        p_number = 'E0000279'
    elif '' in value:
        p_number = 'E0000280'
    elif '' in value:
        p_number = 'E0000281'
    elif '' in value:
        p_number = 'E0000282'
    elif '' in value:
        p_number = 'E0000283'
    elif '' in value:
        p_number = 'E0000284'
    elif '' in value:
        p_number = 'E0000285'
    elif '' in value:
        p_number = 'E0000286'
    elif '' in value:
        p_number = 'E0000287'
    elif '' in value:
        p_number = 'E0000288'
    elif '' in value:
        p_number = 'E0000289'
    elif '' in value:
        p_number = 'E0000290'
    elif '' in value:
        p_number = 'E0000291'
    elif '' in value:
        p_number = 'E0000292'
    else:
        p_number = ''
    return p_number

# 获取js内容
def get_js():
    # f = open("D:/WorkSpace/MyWorkSpace/jsdemo/js/des_rsa.js",'r',encoding='UTF-8')
    f = open("./js/des_rsa.js", 'r', encoding='UTF-8')
    line = f.readline()
    htmlstr = ''
    while line:
        htmlstr = htmlstr + line
        line = f.readline()
    return htmlstr