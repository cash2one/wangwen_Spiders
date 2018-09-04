# # -*- coding: utf-8 -*-
# import requests
# import urllib.request
# import json
#
# url = 'https://book.qidian.com/ajax/comment/index?_csrfToken=HUc4mzWMTveOYkK01P9mREV04r5f0zisvnDNZl7j&bookId=1010191960&pageSize=15'
#
# # headers = {
# #     # "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
# #     # "Accept-Encoding" : "gzip, deflate, br",
# #     # "Accept-Language" : "zh-CN,zh;q=0.9,en;q=0.8",
# #     # "Cache-Control" : "max-age=0",
# #     # "Connection" : "keep-alive",
# #     "Cookie" : "e1=%7B%22pid%22%3A%22qd_P_xiangqing%22%2C%22eid%22%3A%22qd_A64%22%2C%22l1%22%3A40%7D; e2=%7B%22pid%22%3A%22qd_P_xiangqing%22%2C%22eid%22%3A%22qd_A70%22%2C%22l1%22%3A40%7D; _csrfToken=HUc4mzWMTveOYkK01P9mREV04r5f0zisvnDNZl7j; pgv_pvi=8068539392; _qddaz=QD.5fn8uk.gtwx6l.jkulfgif; qdrs=0%7C3%7C0%7C0%7C1; qdgd=1; newstatisticUUID=1534416560_1809913195; rcr=3347812%2C1009915605; ywkey=ywKN7Cp1wLxC; ywguid=854008036544; e1=%7B%22pid%22%3A%22qd_P_all%22%2C%22eid%22%3A%22qd_B58%22%2C%22l1%22%3A5%7D; e2=%7B%22pid%22%3A%22qd_P_all%22%2C%22eid%22%3A%22qd_B15%22%2C%22l2%22%3A1%2C%22l1%22%3A4%7D",
# #     # "Host" : "book.qidian.com",
# #     # "Referer" : "https://www.qidian.com/all",
# #     # "Upgrade-Insecure-Requests" : "1",
# #     "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36",
# # }
# a = requests.get(url)
# print(a.status_code)
# print(json.loads(a.text))
# with open('qidian.txt', "wb") as f:  # 开始写文件，wb代表写二进制文件
#     f.write(a.content)

# response = urllib.request.urlopen(url)
# # 读取网页源码
# html = response.read().decode('utf-8')
#
# print(html)