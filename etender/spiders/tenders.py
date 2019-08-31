# -*- coding: utf-8 -*-
import scrapy
from etender.items import EtenderItem, FileItem
import itertools


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
        url = "https://etenders.treasury.gov.za/views/ajax"
        formdata = {
            "view_name": "search_tender_published",
            "view_display_id": "block_2",
        }
        # for field, options in fieldoptions.items():
        #   for option in options:
        print(list(product_dict(**field_options)))

        #    formdata[f"field_{field_snakecase}_tid"] = option[0]
        #   yielf scrapy.http.FormRequest(url, self.parse_advertised, "POST", formdata)

    def parse_advertised_filter_result(self, response):
        pass


def product_dict(**kwargs):
    keys = kwargs.keys()
    vals = kwargs.values()
    for instance in itertools.product(*vals):
        yield dict(zip(keys, instance))
