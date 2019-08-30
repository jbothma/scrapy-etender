# -*- coding: utf-8 -*-
import scrapy
from etender.items import EtenderItem, FileItem


class TendersSpider(scrapy.Spider):
    name = "tenders"
    allowed_domains = ["etenders.treasury.gov.za"]
    start_urls = ["https://etenders.treasury.gov.za/content/advertised-tenders"]

    def parse(self, response):
        if response.url.endswith("/content/advertised-tenders"):
            self.parse_advertised(response)

    def parse_advertised(self, response):
        fields = ["tender-category", "region", "sector", "testing-dept", "tender-type"]
        field_options = {}
        for field in fields:
            field_option_elements = response.css(f"#edit-field-{field}-tid option")
            field_options[field] = [
                (o.xpath("@value").get(), o.xpath("text()").get())
                for o in field_option_elements
            ]
