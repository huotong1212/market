# -*- coding: utf-8 -*-
import json
import re

import scrapy
from scrapy import cmdline, Request, Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapy_demo.items import GoodItem


class JdSpider(scrapy.Spider):
    name = 'jd'
    allowed_domains = ['jd.com']
    # start_urls = ['http://jd.com/']
    # cookie_dic = None

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
        start_urls = ['https://search.jd.com/Search?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page={}&s=1&click=0'
                          .format(str(i)) for i in range(1,150,2)]
        for url in start_urls:
            yield Request(url=url,callback=self.parse,method='GET')

    # 拿到搜索手机界面的每个商品的ID
    def parse(self, response):
        print('---parse',response)
        goods_list = Selector(response=response).xpath('//ul[@class="gl-warp clearfix"]/li')
        for good in goods_list:
            good_info = {}
            good_id = good.xpath('./@data-pid').extract_first()
            print('good_id___for',good_id)

            sku = good.xpath('./@data-sku').extract_first()
            good_info['id'] = good_id
            # class="J_100005236836" data-sku
            good_price = good.xpath('.//strong[@class="J_{}"]/i/text()'.format(sku)).extract_first()
            good_info['price'] = good_price
            good_name = good.xpath('.//div[@class="p-name p-name-type-2"]//em/text()').extract_first().strip()
            good_info['name'] = good_name
            # id="J_comment_5912071"
            # commnent_count = good.xpath('.//a[@id="J_comment_{}"]'.format(sku))
            # good_info['comment_count'] = commnent_count

            # 直接去抓取评论数，但是有缺陷
            url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3910&productId={}&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1'\
                .format(good_id)

            yield Request(url=url,callback=self.parse_good,meta={'good_info':good_info})

    # 直接发送请求到每个商品到评论，并针对页数发起请求
    def parse_comment(self,response):
        print('---parse_good',response,response.text)
        t = re.findall('^fetchJSON_comment98vv\d*\((.*)\);', response.text)
        json_data = json.loads(t)
        max_page = int(json_data['max_page'])
        good_info = response.meta['good_info']
        id = good_info['id']

        urls = ['https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv3910&productId={}&score=0&sortType=5&page={}&pageSize=10&isShadowSku=0&rid=0&fold=1'
                    .format(id,str(i)) for i in range(max_page)]

        for url in urls:
            yield Request(url = url,callback = self.parse_body,meta={'good_info':good_info})


    def parse_body(self,response):
        print('----parse_body',response,response.text)





if __name__ == "__main__":
    cmdline.execute("scrapy crawl jd --nolog".split())