# -*- coding: utf-8 -*-
# 纪家保险 new_Column13
import json
import pickle
from collections import deque

import pymysql
import scrapy
from scrapy.http import FormRequest
from pymysql.cursors import SSCursor
from scrapy import log

from jijia.items import JijiaItem


class JiJiaSpider(scrapy.Spider):
    name = 'jijia'
    error_count = 0
    record_file = 'jijia_record.pickle'

    url = 'https://jijia-api-bj01.tuofeng.cn/oauth/token'

    def start_requests(self):
        try:
            with open(self.record_file, 'rb') as f:
                record = pickle.load(f)
        except Exception:
            record = deque(maxlen=10)  # 最近10条运行状态

        if len(record) == 0:
            start_pos = 0
        else:
            start_pos = record.pop()

        total_rows = 35763722  # 记录的总长度
        step = 50

        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='root',
                               db='dafy', charset='utf8', cursorclass=SSCursor)
        cur = conn.cursor()

        while start_pos < total_rows:

            sql = "SELECT phone_number, customer_type from hangjiabao_backup" \
                  " where customer_type='contact' limit %d, %d" % (start_pos, step)
            try:
                cur.execute(sql)
            except Exception:
                self.error_count += 1
                if self.error_count > 3:
                    with open(self.record_file, 'wb') as f:
                        pickle.dump(record, f)
                    break
                else:
                    continue

            for phone, customer_type in cur:
                form = {
                    'grant_type': 'client_credentials',
                    'provider': 'jijia_mobile',
                    'appid': 'jijia_mobile',
                    'client_id': phone,
                    'client_secret': '123456RvA'
                }

                yield FormRequest(self.url, formdata=form, callback=self.parse,
                                  meta={'phone': phone, 'customer_type': customer_type})

            record.append(start_pos)

            print('-------------------------------------------------')
            print(record)
            print('-------------------------------------------------')

            with open(self.record_file, 'wb') as f:
                pickle.dump(record, f)

            start_pos = start_pos + step

    def parse(self, response):
        try:
            res = json.loads(response.text)
            log.msg(res, level=log.INFO)
        except Exception as e:
            raise e

        item = JijiaItem()
        # not register:
        # {"result": false, "msg": "手机号未注册"}

        # register:
        # {"code":400,"error":"invalid_grant","error_description":"Client credentials are invalid"}
        if res.get('error') == 'invalid_grant':
            item['isRegister'] = 1
        else:
            item['isRegister'] = 0

        item['phone_number'] = response.meta['phone']
        item['customer_type'] = response.meta['customer_type']

        return item


