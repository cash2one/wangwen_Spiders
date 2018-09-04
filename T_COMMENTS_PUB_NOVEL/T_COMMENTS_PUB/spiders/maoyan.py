# -*- coding: utf-8 -*-
import requests
from lxml import etree

url = 'http://catdot.dianping.com/broker-service/commandbatch'
data = {
    'r': '1532945286000',
    'v': '5',
    'p': '12',
    'unionId': '4AE4D4D6C72B0E126872A0E039D9BF18DA6995A6605C0830BA0D5C856C07085D',
    'av': '841',
}
sel = requests.post(url, data=data)
# response = etree.HTML(sel.text)
print(sel.status_code, sel.text,'================')
