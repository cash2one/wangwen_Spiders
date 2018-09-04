# -*- coding: utf-8 -*-

from scrapy import cmdline
import os
os.chdir("T_NOVEL_SUMMARY/spiders")
# cmdline.execute('scrapy crawl jjwxc'.split())
# cmdline.execute('scrapy crawl shuqi'.split())
# cmdline.execute('scrapy crawl 17k'.split())
# cmdline.execute('scrapy crawl ireader'.split())
# cmdline.execute('scrapy crawl zongheng'.split())
# cmdline.execute('scrapy crawl yunqi_qq'.split())
# cmdline.execute('scrapy crawl chuangshi_qq'.split())
# cmdline.execute('scrapy crawl book_qq'.split())
# cmdline.execute('scrapy crawl qidian'.split())
cmdline.execute('scrapy crawl qidian_2'.split())
# cmdline.execute('scrapy crawl 3gsc'.split())
# cmdline.execute('scrapy crawl heiyan'.split())
# cmdline.execute('scrapy crawl hongshu'.split())
# cmdline.execute('scrapy crawl hongxiu'.split())
# cmdline.execute('scrapy crawl yuedu163'.split())
# cmdline.execute('scrapy crawl xiang5'.split())