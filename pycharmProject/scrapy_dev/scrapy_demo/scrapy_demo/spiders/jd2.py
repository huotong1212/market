# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options



class Jd2Spider(scrapy.Spider):
    name = 'jd2'
    allowed_domains = ['https://search.jd.com/']
    # start_urls = ['http://jd2.com/']

    def __init__(self):
        print('spider init')
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        # 设置无头版本的Chrome
        self.browser = webdriver.Chrome(chrome_options=self.chrome_options)
        # Set the amount of time to wait for a page load to complete
        # before throwing an error.
        self.browser.set_page_load_timeout(30)

    def close(spider, reason):
        print('spider closed',reason)
        spider.call_close()
        spider.browser.close()


    def start_requests(self):
        print('start request')
        urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page={}&s=1&click=0'
                    .format(str(i)) for i in range(1,4,2)]

        for url in urls:
            yield Request(url=url,callback = self.parse)

    def parse(self, response):
        print('---parse')
        goods = Selector(response=response).xpath('//ul[@class="gl-warp clearfix"]/li')
        print('len',len(goods))

if __name__ == "__main__":
    from scrapy import cmdline
    cmdline.execute("scrapy crawl jd2 --nolog".split())