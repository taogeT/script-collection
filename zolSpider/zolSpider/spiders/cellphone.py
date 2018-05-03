# -*- coding: utf-8 -*-
from . import BaseZolSpider


class CellphoneSpider(BaseZolSpider):
    name = 'cellphone'
    start_urls = ['http://detail.zol.com.cn/cell_phone_index/subcate57_list_1.html']
