# -*- coding: utf-8 -*-
from . import BaseZolSpider


class NotebookSpider(BaseZolSpider):
    name = 'notebook'
    start_urls = ['http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_0_1_2_0_1.html']
