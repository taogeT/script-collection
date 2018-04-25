# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import xlsxwriter


class ZolspiderPipeline(object):

    def __init__(self):
        self.table_dict = {}

    def close_spider(self, spider):
        if len(self.table_dict.keys()) > 0:
            workbook = xlsxwriter.Workbook('ZOL-' + datetime.now().strftime('%Y%m%d-%H%M%S') + '.xlsx')
            worksheet = workbook.add_worksheet(name='ZOL 遍历结果')

            for keyIndex, (key, valueArray) in enumerate(self.table_dict.items()):
                worksheet.write(0, keyIndex, key)
                for valueIndex, value in enumerate(valueArray):
                    worksheet.write(valueIndex + 1, keyIndex, value)

            workbook.close()

    def process_item(self, item, spider):
        self.table_dict.setdefault('名称', []).append(item['name'])
        self.table_dict.setdefault('价格', []).append(item['price'])
        for key, value in item['params'].items():
            self.table_dict.setdefault(key, []).append(value)
