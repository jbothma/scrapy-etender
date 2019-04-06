# -*- coding: utf-8 -*-
import scrapy
from etender.items import EtenderItem, FileItem


class TendersSpider(scrapy.Spider):
    name = 'tenders'
    allowed_domains = ['etenders.treasury.gov.za']
    start_urls = ['https://etenders.treasury.gov.za/content/advertised-tenders']

    def parse(self, response):
        some_tender_row_title = response.css('td.views-field-title')[0]
        tender_table = some_tender_row_title.xpath('../..')
        for tender_row in tender_table.xpath('tr'):
            url = tender_row.css('td.views-field-title a::attr(href)').get()
            published_selector = 'td.views-field-field-date-published span::attr(content)'
            briefing_selector = 'td.views-field-field-compulsory-briefing-sessio::text'
            closing_date_selector = 'td.views-field-field-closing-date span::attr(content)'
            meta = {
                'category': tender_row.css('td.views-field-field-tender-category::text').get().strip(),
                'description_short': tender_row.css('td.views-field-title a::text').get().strip(),
                'number': tender_row.css('td.views-field-field-code::text').get().strip(),
                'date_published': tender_row.css(published_selector).get().strip(),
                'closing_time_and_date': tender_row.css(closing_date_selector).get().strip(),
                'compulsory_briefing_session': tender_row.css(briefing_selector).get().strip(),
            }
            yield scrapy.Request(response.urljoin(url),
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
        etender['category'] = response.meta['category']
        etender['description_short'] = response.meta['description_short']
        etender['number'] = response.meta['number']
        etender['date_published'] = response.meta['date_published']
        etender['closing_time_and_date'] = response.meta['closing_time_and_date']
        etender['compulsory_briefing_session'] = response.meta['compulsory_briefing_session']
        etender['free_text'] = response.css('div.field-name-field-econtact').get()

        yield etender
