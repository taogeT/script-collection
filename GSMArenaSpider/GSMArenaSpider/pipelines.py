# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

import xlsxwriter
import codecs
import json


class GsmarenaExcelPipeline(object):

    def __init__(self):
        self.column_list = ['Name']
        self.dict_list = []

    def close_spider(self, spider):
        if len(self.dict_list) > 0:
            workbook = xlsxwriter.Workbook('Gsmarena-{}-{}.xlsx'.format(spider.name, datetime.now().strftime('%Y%m%d%H%M')))
            worksheet = workbook.add_worksheet(name='Gsmarena 遍历结果')
            # write column name
            for columnIndex, column in enumerate(self.column_list):
                worksheet.write(0, columnIndex, column)
            # write row
            for rowIndex, row in enumerate(self.dict_list):
                for rowKey, rowValue in row.items():
                    worksheet.write(rowIndex + 1, self.column_list.index(rowKey), rowValue)
            workbook.close()

    def process_item(self, item, spider):
        self.dict_list.append(dict(item['params'], Name=item['name']))
        self.column_list += [key for key in item['columns'] if key not in self.column_list]
        return item


class GsmarenaJsonPipeline(object):

    def __init__(self):
        self.dict_list = []

    def close_spider(self, spider):
        if len(self.dict_list) > 0:
            with codecs.open('Gsmarena-{}-{}.json'.format(spider.name, datetime.now().strftime('%Y%m%d%H%M')), 'w', encoding='utf-8') as fw:
                json.dump(self.dict_list, fw, ensure_ascii=False)

    def process_item(self, item, spider):
        self.dict_list.append(dict(item['params'], Name=item['name']))
        return item
