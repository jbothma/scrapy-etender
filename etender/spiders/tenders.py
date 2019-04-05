# -*- coding: utf-8 -*-
import scrapy
from etender.items import EtenderItem, FileItem


class TendersSpider(scrapy.Spider):
    name = 'tenders'
    allowed_domains = ['etenders.treasury.gov.za']
    start_urls = ['https://etenders.treasury.gov.za/content/advertised-tenders']

    def parse(self, response):
        for tender_url in response.css('td.views-field-title a::attr(href)').getall():
            meta = {
                'description_short': response.css('td.views-field-title a::text').get(),
            }
            yield scrapy.Request(response.urljoin(tender_url),
                                 callback=self.parse_tender,
                                 meta=meta
            )

        next_page = response.css('li.pager-next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)

    def parse_tender(self, response):
        etender = EtenderItem()
        etender['url'] = response.url
        etender['description_short'] = response.meta['description_short']

        yield etender
