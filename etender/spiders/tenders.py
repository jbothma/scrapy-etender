# -*- coding: utf-8 -*-
import scrapy
from etender.items import EtenderItem, FileItem
import itertools
import json


class TendersSpider(scrapy.Spider):
    name = "tenders"
    allowed_domains = ["etenders.treasury.gov.za"]

    def start_requests(self):
        yield scrapy.Request(
            "https://etenders.treasury.gov.za/content/advertised-tenders",
            callback=self.parse_search_start
        )

    def parse_search_start(self, response):
        field_options = get_select_options("testing-dept", response)
        for option in field_options:
            if option["value"] == "All":
                continue
            if option["label"] != "ESKOM":
                continue
            yield self.create_search_request(option, page=0)

    def parse_advertised(self, response):
        print(response.meta["department_option"]["label"])
        response_list = json.loads(response.body_as_unicode())
        insert_command = [c for c in response_list if c["command"] == "insert"][0]
        html = insert_command["data"]
        html_response = scrapy.http.HtmlResponse(url="", body=html.encode("utf-8"))
        for title in html_response.css(".views-field-title").xpath(".//a/text()").getall():
            print("  %s" % title)

    def create_search_request(self, department_option, page):
        url = "https://etenders.treasury.gov.za/views/ajax"
        formdata = {
            "field_tender_category_tid": "All",
            "field_region_tid": "All",
            "field_sector_tid": "All",
            "field_testing_dept_tid": department_option["value"],
            "field_tender_type_tid": "All",
            "view_name": "search_tender_published",
            "view_display_id": "block_2",
            "view_path": "node/42",
            "view_base_path": "search_tender_published",
            "page": str(0),
        }
        meta = {
            "department_option": department_option,
        }
        return scrapy.http.FormRequest(
            url,
            formdata=formdata,
            callback=self.parse_advertised,
            method="POST",
            meta=meta
        )


def get_select_options(field_name, response):
    field_option_elements = response.css(f"#edit-field-{field_name}-tid option")
    return [
        {
            "value": o.xpath("@value").get(),
            "label": o.xpath("text()").get(),
        }
        for o in field_option_elements
    ]
