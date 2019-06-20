# -*- coding: utf-8 -*-
import datetime

import scrapy
from scrapy import Request
from scrapy.http import Response


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['https://www.lagou.com']
    start_urls = ['http://lagou.com/']

    now = datetime.datetime.now()
    timeStamp = int(now.timestamp() * 1000)
    geshi = "%Y%m%d%H%M%S"
    time1 = datetime.datetime.strftime(now, geshi)

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "keep-alive",
        "Host": "m.lagou.com",
        "Cookie": "_ga=GA1.2.841469794.1541152606; user_trace_token=20181102175657-a2701865-de85-11e8-8368-525400f775ce; LGUID=20181102175657-a2701fbd-de85-11e8-8368-525400f775ce; index_location_city=%E5%B9%BF%E5%B7%9E; _gid=GA1.2.311675459.1542615716; _ga=GA1.3.841469794.1541152606; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1542634073,1542634080,1542634122,1542634128; JSESSIONID=ABAAABAAAGCABCC1B87E5C12282CECED77A736D4CD7FA8A; X_HTTP_TOKEN=aae2d9e96d6a68f72d98ab409a933460; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221672c5c65c01c7-0e8e56366a6cce-3a3a5c0e-2073600-1672c5c65c3bf%22%2C%22%24device_id%22%3A%221672c5c65c01c7-0e8e56366a6cce-3a3a5c0e-2073600-1672c5c65c3bf%22%7D; sajssdk_2015_cross_new_user=1; _gat=1; LGSID=20181119231628-167f7db1-ec0e-11e8-a76a-525400f775ce; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fm.lagou.com%2Fsearch.html; PRE_LAND=https%3A%2F%2Fm.lagou.com%2Fjobs%2F5219979.html; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6={timeStamp}; LGRID={time}-1c458fde-ec0e-11e8-895f-5254005c3644".format(
            timeStamp=timeStamp, time=time1),
        "Referer": "https://m.lagou.com/search.html",
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
    }

    def start_requests(self):
        for i in range(100):
            print("开始爬取第{}页".format(i + 1))
            base_url = "https://m.lagou.com/search.json?city={city}&positionName={positionName}&pageNo={pageNo}&" \
                       "pageSize={pageSize}".format(city='深圳', positionName='python', pageNo=str(i),
                                                    pageSize=str(15))
            yield Request(url=base_url,callback=self.parse,headers=LagouSpider.headers)


    def parse(self, response):
        print('---------parse',response)
        print(response.text)

if __name__ == "__main__":
    from scrapy import cmdline
    cmdline.execute("scrapy crawl lagou --nolog".split())