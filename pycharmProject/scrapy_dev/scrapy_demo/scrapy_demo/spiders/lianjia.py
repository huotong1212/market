# -*- coding: utf-8 -*-
import json
from urllib.parse import quote

import scrapy
from scrapy import Request, Selector

from scrapy_demo.items import LianjiaItem


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['lianjia.com']
    # start_urls = ['https://nj.lianjia.com/']

    name = 'lianjia'
    allowed_domains = ['nj.lianjia.com']
    regions = {'gulou':'鼓楼',
               'jianye':'建邺',
               'qinhuai':'秦淮',
               'xuanwu':'玄武',
               'yuhuatai':'雨花台',
               'qixia':'栖霞',
               'jiangning':'江宁',
               'liuhe':'六合',
               'pukou':'浦口',
               'lishui':'涟水',
               'gaochun':'高淳'
    }

    # 重写start_request方法，获取所有地级区的所有小区界面
    def start_requests(self):
        for i,region in enumerate(list(self.regions.keys())):
            # url = "https://nj.lianjia.com/xiaoqu/" + region + "/"
            url = "https://nj.lianjia.com/xiaoqu/{}/".format(region)
            if i == 1:
                break
        # url = "https://www.baidu.com/"
            yield Request(url=url,
                          method="GET",
                          # headers={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"},
                          callback=self.parse,
                          meta={'region': region})

        # for region in list(self.regions.keys()):
        #     url = "https://nj.lianjia.com/xiaoqu/" + region + "/"
        #     yield Request(url=url, callback=self.parse, meta={'region': region})  # 用来获取页码


    # 获取每一页的页面信息
    def parse(self, response):
        region = response.meta['region']
        # 获取page-data="{"totalPage":30,"curPage":1}"
        page_data = Selector(response=response).\
            xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()  # 标签对象列表
        page_data = json.loads(page_data)
        for i in range(page_data["totalPage"]):
            url = "https://nj.lianjia.com/xiaoqu/{}/pg{}/".format(region, str(i+1))
            yield Request(url=url,method="GET",callback=self.parse_xiaoqu,meta={'region':response.meta['region']})

    # 进入到每一个小区中的成交房源信息，获取每个小区的名字，然后yield到小区成交页面
    # url = "https://nj.lianjia.com/chengjiao/rs" + quote(xq_name) + "/"
    # class="listContent"
    def parse_xiaoqu(self, response):
        xiaoqu_names = Selector(response=response). \
            xpath('//ul[@class="listContent"]//div[@class="title"]/a/text()').extract()
        i = 0
        for name in xiaoqu_names:
            i += 1
            if i >3:
                break
            # URL只允许一部分ASCII字符,使用quote进行转码
            url = "https://nj.lianjia.com/chengjiao/rs" + quote(name) + "/"
            yield Request(url=url,method="GET",callback=self.parse_chengjiao
                          , meta={'name':name,'region':response.meta['region']})
            # item = LianjiaItem()
            # yield item

    # 获取这个页面的所有页码的链接
    def parse_chengjiao(self, response):
        name = response.meta['name']
        page_url = Selector(response=response).\
            xpath('//div[@class="page-box house-lst-page-box"]/@page-url').extract_first()
        # 获取page-data="{"totalPage":30,"curPage":1}"
        page_data = Selector(response=response). \
            xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract_first()  # 标签对象列表
        page_data = json.loads(page_data)
        deal_list = Selector(response=response).xpath('//ul[@class="listContent"]/li')

        if page_data["totalPage"]>1:
            for i in range(page_data["totalPage"]):
                # /chengjiao/pg{page}rs%E6%96%B0%E6%B2%B3%E4%B8%80%E6%9D%91/
                page = page_url.replace('{page}', str(i+1),1)
                url = "https://nj.lianjia.com{}".format(page)
                print('page_cs_url', url)
                yield Request(url=url, method="GET", callback=self.parse_content, meta=response.meta)
        else:
            item_list = self.package(deal_list, dict(response.meta))
            for item in item_list:
                yield item

    # 获取这个页面的所有房源信息
    def parse_content(self, response):
        deal_list = Selector(response=response).xpath('//ul[@class="listContent"]/li')
        item_list = self.package(deal_list, dict(response.meta))
        for item in item_list:
            yield item

    def package(self,deal_list, meta):
        item_list = []
        for cj in deal_list:
            item = LianjiaItem()
            item['region'] = self.regions.get(meta['region'])
            href = cj.xpath('./a/@href').extract()
            if not len(href):
                continue
            item['href'] = href[0]

            content = cj.xpath('.//div[@class="title"]/a/text()').extract()
            if len(content):
                content = content[0].split()  # 按照空格分割成一个列表
                item['name'] = content[0]
                item['style'] = content[1]
                item['area'] = content[2]
            content = cj.xpath('.//div[@class="houseInfo"]/text()').extract()
            if len(content):
                content = content[0].split('|')
                item['orientation'] = content[0]
                item['decoration'] = content[1]
                if len(content) == 3:
                    item['elevator'] = content[2]
                else:
                    item['elevator'] = '无'

            content = cj.xpath('.//div[@class="positionInfo"]/text()').extract()
            if len(content):
                content = content[0].split()
                item['floor'] = content[0]
                if len(content) == 2:
                    item['build_year'] = content[1]
                else:
                    item['build_year'] = '无'

            content = cj.xpath('.//div[@class="dealDate"]/text()').extract()
            if len(content):
                item['sign_time'] = content[0]

            content = cj.xpath('.//div[@class="totalPrice"]/span/text()').extract()
            if len(content):
                item['total_price'] = content[0]

            content = cj.xpath('.//div[@class="unitPrice"]/span/text()').extract()
            if len(content):
                item['unit_price'] = content[0]

            content = cj.xpath('.//span[@class="dealHouseTxt"]/span/text()').extract()
            if len(content):
                for i in content:
                    if i.find("房屋满") != -1:  # 找到了返回的是非-1得数，找不到的返回的是-1
                        item['fangchan_class'] = i
                    elif i.find("号线") != -1:
                        item['subway'] = i
                    elif i.find("学") != -1:
                        item['school'] = i

        print('item',item.items())
        item_list.append(item)
        return item_list

if __name__ == "__main__":
    from scrapy import cmdline
    cmdline.execute("scrapy crawl lianjia --nolog".split())