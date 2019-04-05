# -*- coding: utf-8 -*-
import scrapy


class TendersSpider(scrapy.Spider):
    name = 'tenders'
    allowed_domains = ['etenders.treasury.gov.za']
    start_urls = ['https://etenders.treasury.gov.za/content/advertised-tenders']

    def parse(self, response):
        next_page = response.css('li.pager-next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
