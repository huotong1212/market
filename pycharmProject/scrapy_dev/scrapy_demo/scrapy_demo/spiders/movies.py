# -*- coding: utf-8 -*-
from xml import etree

import scrapy
from scrapy import Spider, Request, Selector

from scrapy_demo.items import SanshengItem


class movies(Spider):
    '''
    这个是三生三世十里桃花
    '''
    name = 'movies'

    def start_requests(self):
        templateurl = 'https://movie.douban.com/subject/25823277/comments?start={}&limit=20&sort=new_score&status=P'
        for i in range(3201):
            url = templateurl.format(str(i * 20))
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        selector = Selector(response=response)
        item = SanshengItem()
        item['comments'] = selector.xpath('//div[@class="comment"]/p/text()').extract()
        print(item.items())
        yield item

if __name__ == "__main__":
    from scrapy import cmdline
    cmdline.execute("scrapy crawl movies --nolog".split())