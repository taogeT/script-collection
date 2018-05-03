# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import xlsxwriter
import codecs
import json


class ZolspiderExcelPipeline(object):

    def __init__(self):
        self.table_dict = {}

    def close_spider(self, spider):
        if len(self.table_dict.keys()) > 0:
            workbook = xlsxwriter.Workbook('ZOL-{}-{}.xlsx'.format(spider.name, datetime.now().strftime('%Y%m%d-%H%M%S')))
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
        return item


class ZolspiderJsonPipeline(object):

    def __init__(self):
        self.dict_list = []

    def close_spider(self, spider):
        if len(self.dict_list) > 0:
            with codecs.open('ZOL-{}-{}.json'.format(spider.name, datetime.now().strftime('%Y%m%d%H%M%S')), 'w', encoding='utf-8') as fw:
                json.dump(self.dict_list, fw, ensure_ascii=False)

    def process_item(self, item, spider):
        self.dict_list.append(dict(item['params'], 名称=item['name'], 价格=item['price']))
        return item
