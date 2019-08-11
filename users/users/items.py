# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UsersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    mid = scrapy.Field()    #用户id
    name = scrapy.Field()   #用户昵称
    sex = scrapy.Field()    #性别
    sign = scrapy.Field()   #签名
    face = scrapy.Field()   #头像地址
    level = scrapy.Field()  #等级
    coins = scrapy.Field()  #硬币
    birthday = scrapy.Field() #生日
