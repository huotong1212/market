# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Request, Selector

from scrapy_demo.items import CommentItem


class MoviesSpider(scrapy.Spider):
    name = 'avengers'
    allowed_domains = ['movie.douban.com']
    base_url = "https://movie.douban.com/subject/26100958/comments"
    start_urls = [base_url]

    # def start_requests(self):
    #     yield Request(url=self.base_url,method="GET",callback=self.parse)

    def parse(self, response):
        # self.parse_comment(response)
        i = 1
        print('first i',i)
        item_list = self.parse_comment(response) # 会先执行第一个yield，再执行下一个
        for item in item_list:
            yield item
        # yield item
        # 拿到下一页
        # ?start=40&limit=20&sort=new_score&status=P&percent_type=
        i += 1
        print('second i',i)
        next_page = Selector(response=response).\
            xpath('//div[@id="paginator"]/a[@class="next"]/@href').extract_first()
        next_page = self.base_url + re.match('^\?.*status=P',next_page).group()
        yield Request(url=next_page,method="GET",callback=self.parse)

    def parse_comment(self,response):
        print('---parse_comment')
        all_comments = Selector(response=response).\
            xpath('//div[@id="comments"]/div[@class="comment-item"]')
        item_list = []
        for comment in all_comments:
            item = CommentItem()
            substance = comment.xpath('.//span[@class="votes"]/text()').extract()
            if len(substance):
                item['votes'] = substance[0]

            substance = comment.xpath('./div[@class="avatar"]/a/@title').extract()
            if len(substance):
                item['title'] = substance[0]

            substance = comment.xpath('.//span[@class="rating"]/@class').extract()
            if len(substance):
                item['rating_id'] = substance[0]

            substance = comment.xpath('.//span[@class="rating"]/@title').extract()
            if len(substance):
                item['rating'] = substance[0]

            substance = comment.xpath('.//span[@class="comment-time "]/@title').extract()
            if len(substance):
                item['time'] = substance[0]

            substance = comment.xpath('.//span[@class="short"]/text()').extract()
            if len(substance):
                item['content'] = substance[0]

            item_list.append(item)
        return item_list

if __name__ == "__main__":
    from scrapy import cmdline
    cmdline.execute("scrapy crawl avengers --nolog".split())
