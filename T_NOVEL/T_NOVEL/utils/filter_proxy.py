from Mydb import Mydb
import requests

class ProxyManager(object):
    def __init__(self, mydb):
        self.mydb = mydb
        self.base_url = 'http://www.baidu.com'

    def drop_ip(self,proxy_ip):
        print('删除代理：%s' % proxy_ip)
        sql = 'delete from proxy_gaoni_2 where proxy_ip="%s"' % proxy_ip
        self.mydb.exe(sql)

    def filter_proxy(self):
        sql = 'select * from proxy_gaoni_2'
        res = self.mydb.query(sql)
        for item in res:
            proxy = {
                'http' : '%s://%s:%s' % (item[2],item[0],item[1]),
                'https' : '%s://%s:%s' % (item[2],item[0],item[1])
            }
            try:
                response = requests.get(self.base_url,timeout=6,proxies=proxy)
                print(response.status_code)
            except Exception as e:
                print('请求失败: %s' % (str(e)))
                # 从数据库中删除不可用代理
                self.drop_ip(item[0])
            else:
                if not (200 <= response.status_code <= 300):
                    self.drop_ip(item[0])


if __name__ == '__main__':
    mydb = Mydb('127.0.0.1', 'root', 'root', 'mydb', charset='utf8')
    pm = ProxyManager(mydb)
    pm.filter_proxy()
