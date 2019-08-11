# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging

from pymysql import cursors
from twisted.enterprise import adbapi
import time
'''
class UsersPipeline(object):
    def process_item(self, item, spider):
        return item
'''
class UsersPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        db_parmars = {
            'host': settings['MYSQL_HOST'],
            'user': settings['MYSQL_USER'],
            'passwd': settings['MYSQL_PASSWORD'],
            'db': settings['MYSQL_DBNAME'],
            'port': settings['MYSQL_PORT'],
            'charset': settings['MYSQL_CHARSET'],
        }
        dbpool = adbapi.ConnectionPool('pymysql', **db_parmars)
        return cls(dbpool)

    def process_item(self, item, spider):
        query = self.dbpool.runInteraction(
            self.insert_data_to_mysql,
            item
        )
        query.addErrback(
            self.insert_err,
            spider
        )

        return item

    def insert_data_to_mysql(self, cursor, item):
        #sql = "insert into user(mid, name, sex, sign, face, coins, birthday, level) VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')".format(item['mid'],item['name'],item['sex'],item['sign'],item['face'],item['coins'],item['birthday'],item['level'])
        sql = """
        insert into user(mid, name, sex, sign, face, coins, birthday, level) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """
        args = (item['mid'],item['name'],item['sex'],item['sign'],item['face'],item['coins'],item['birthday'],item['level'])

        cursor.execute(sql,args)

    def insert_err(self, failure, item):
        print(failure, '失败', item)




