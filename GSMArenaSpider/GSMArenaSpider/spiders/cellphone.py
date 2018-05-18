# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from ..items import ProductItem


class CellphoneSpider(Spider):
    name = 'cellphone'
    allowed_domains = ['gsmarena.com']
    start_urls = ['https://www.gsmarena.com/makers.php3']

    def parse(self, response):
        for band_element in response.xpath('//div[@class="st-text"]/table/tr/td/a'):
            yield Request(response.urljoin(band_element.xpath('@href').extract_first()),
                          callback=self.parse_list, priority=10)

    def parse_list(self, response):
        next_url = response.xpath('//div[contains(@class, "pages-next-prev")]/a[@class="pages-next"]/@href').extract_first()
        if next_url:
            yield Request(response.urljoin(next_url), callback=self.parse, priority=10)
        for product_el in response.xpath('//div[@class="section-body"]/div/ul/li/a'):
            yield Request(response.urljoin(product_el.xpath('@href').extract_first()),
                          callback=self.parse_params, priority=5)

    def parse_params(self, response):
        product_name = response.xpath('//h1[@class="specs-phone-name-title"]/text()').extract_first()
        product_params = {}
        product_columns = []
        name_th_text = ''
        for tr_element in response.xpath('//div[@id="specs-list"]/table/tr'):
            th_text = tr_element.xpath('th/text()').extract_first()
            if not name_th_text or (th_text and name_th_text != th_text):
                name_th_text = th_text

            name_text = tr_element.xpath('td[@class="ttl"]/a/text()').extract_first()
            if not name_text:
                name_text = name_th_text

            param_content = tr_element.xpath('td[@class="nfo"]')
            has_element = param_content.xpath('a').extract_first()
            content_text = param_content.xpath('{}text()'.format('a/' if has_element else '')).extract_first()

            product_params[name_text] = content_text
            product_columns.append(name_text)

        if len(product_columns) > 0:
            yield ProductItem(name=product_name, params=product_params, columns=product_columns)



