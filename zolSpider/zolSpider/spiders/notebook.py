# -*- coding: utf-8 -*-
from functools import reduce
from scrapy import Request
from ..items import ProductItem

import scrapy


class NotebookSpider(scrapy.Spider):
    name = 'notebook'
    allowed_domains = ['detail.zol.com.cn']
    start_urls = ['http://detail.zol.com.cn/notebook_index/subcate16_0_list_1_0_1_2_0_1.html']

    def parse(self, response):
        for notebook_url in response.xpath('//ul[@id="J_PicMode"]/li/a/@href').extract():
            yield Request(response.urljoin(notebook_url), callback=self.parse_notebook)
        next_url = response.xpath('//div[@class="pagebar"]/a[@class="next"]/@href').extract_first()
        if next_url:
            yield Request(response.urljoin(next_url), callback=self.parse)

    def parse_notebook(self, response):
        notebook_name = response.xpath('//h1[@class="product-model__name"]/text()').extract_first()
        notebook_price = response.xpath('//b[@class="price-type"]/text()').extract_first()
        param_url = response.xpath('//a[contains(@class, "_j_MP_more") and contains(@class, "more")]/@href').extract_first()
        if param_url:
            yield Request(response.urljoin(param_url), callback=self.parse_notebook_param, meta={
                '名称': notebook_name, '价格': notebook_price
            })

    def parse_notebook_param(self, response):
        item = ProductItem(name=response.meta['名称'], price=response.meta['价格'], params={})
        for li_index, li_element in enumerate(response.xpath('//ul[@class="category-param-list"]/li')):
            param_name = li_element.xpath('span[@id="newPmName_{}"]/text()'.format(li_index + 1)).extract_first()
            param_content_tag = 'span[@id="newPmVal_{}"]/'.format(li_index + 1)
            has_element = li_element.xpath(param_content_tag + 'a').extract_first()
            if has_element:
                a_text = li_element.xpath(param_content_tag + 'a/text()').extract()
                span_text = li_element.xpath(param_content_tag + 'text()').extract()
                # delete \r\n and split with ，
                span_text = list(map(lambda a: a.replace('\r\n', '').split('，'), span_text))
                # reduce join
                if len(span_text) > 1:
                    span_text = list(filter(lambda x: x, reduce(lambda x, y: x + y, span_text)))
                elif len(span_text) == 1:
                    span_text = span_text[0]

                item['params'][param_name] = '，'.join(a_text + span_text)
            else:
                item['params'][param_name] = li_element.xpath(param_content_tag + 'text()').extract_first()
        yield item
