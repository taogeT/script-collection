# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from functools import reduce
from scrapy import Request, Spider
from ..items import ProductItem


class BaseZolSpider(Spider):

    allowed_domains = ['detail.zol.com.cn']

    def parse(self, response):
        next_url = response.xpath('//div[@class="pagebar"]/a[@class="next"]/@href').extract_first()
        if next_url:
            yield Request(response.urljoin(next_url), callback=self.parse, priority=10)
        for product_el in response.xpath('//ul[@id="J_PicMode"]/li'):
            param_url = product_el.xpath('div[@class="comment-row"]/a[@class="comment-num"]/@href').extract_first()
            if param_url:
                meta_json = {
                    '名称': product_el.xpath('h3/a/text()').extract_first(),
                    '价格': product_el.xpath('div[@class="price-row"]/span/b[@class="price-type"]/text()').extract_first()
                }
                yield Request(response.urljoin(param_url.replace('review.shtml', 'param.shtml')),
                              callback=self.parse_param, meta=meta_json, priority=5)

    def parse_param(self, response):
        item_params = {}
        for li_element in response.xpath('//ul[@class="category-param-list"]/li'):
            param_name, param_content = li_element.xpath('span')
            param_name = param_name.xpath('text()').extract_first()
            has_element = param_content.xpath('a').extract_first()
            if has_element:
                a_text = param_content.xpath('a/text()').extract()
                span_text = param_content.xpath('text()').extract()
                # delete \r\n and split with ，
                span_text = list(map(lambda a: a.replace('\r\n', '').split('，'), span_text))
                # reduce join
                if len(span_text) > 1:
                    span_text = list(filter(lambda x: x, reduce(lambda x, y: x + y, span_text)))
                elif len(span_text) == 1:
                    span_text = span_text[0]

                item_params[param_name] = '，'.join(a_text + span_text)
            else:
                item_params[param_name] = param_content.xpath('text()').extract_first()
        if len(item_params.keys()) > 0:
            item = ProductItem(name=response.meta['名称'], price=response.meta['价格'], params=item_params)
            yield item
