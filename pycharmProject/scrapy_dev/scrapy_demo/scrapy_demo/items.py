# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyDemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

#items.py
from scrapy import Item,Field

class LianjiaItem(Item):
    region = Field()      #行政区域
    href = Field()        #房源链接
    name = Field()        #房源名称
    style = Field()       #房源结构
    area = Field()           #小区
    orientation = Field()    #朝向
    decoration = Field()     #装修
    elevator = Field()       #电梯
    floor = Field()          #楼层高度
    build_year = Field()     #建造时间
    sign_time = Field()      #签约时间
    unit_price = Field()     #每平米单价
    total_price = Field()    #总价
    fangchan_class = Field()   #房产类型
    school = Field()         #周边学校
    subway = Field()         #周边地铁

class CommentItem(Item):
    title = Field()
    content = Field()
    votes = Field()
    rating_id = Field()
    rating = Field()
    time = Field()
    userImage_url = Field()  # 用户头像图片
    userImage_path = Field() # 头像本地保存路径

class SanshengItem(Item):
    price = Field()
    name = Field()
    comments = Field()

class GoodItem(Item):
    id = Field()
    name = Field()
    price = Field()
    comment_count = Field()
    comments = Field()


class GoodCommentItem(Item):
    userId = Field()
    userName = Field()
    content = Field()
    datatime = Field()
    star = Field()
