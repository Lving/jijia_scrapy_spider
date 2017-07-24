# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
# 纪家保险 new_Column13
import pymysql
from scrapy.exceptions import DropItem


class JijiaPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root',
                                    db='dafy', charset='utf8')

    def process_item(self, item, spider):
        cur = self.conn.cursor()
        phone_number = item['phone_number']
        isRegister = item['isRegister']

        # 改存储字段， 很重要!!
        if isRegister:
            sql = "UPDATE hangjiabao_backup SET new_Column13 = %d WHERE phone_number = '%s'" % (isRegister, phone_number)
            cur.execute(sql)
            self.conn.commit()
        else:
            raise DropItem(' %s Not Registered' % item)
        return item

    def __del__(self):
        self.conn.close()

