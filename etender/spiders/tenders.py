# -*- coding: utf-8 -*-
import scrapy
from etender.items import EtenderItem, FileItem
import itertools
import json
import html2text

h = html2text.HTML2Text()


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
            yield self.create_search_request(option, page_number=0)

    def parse_advertised(self, response):
        print(response.meta["department_option"]["label"])
        response_list = json.loads(response.body_as_unicode())
        insert_command = [c for c in response_list if c["command"] == "insert"][0]
        html = insert_command["data"]
        html_response = scrapy.http.HtmlResponse(url="", body=html.encode("utf-8"))
        for row in html_response.css("tr"):
            if not row.css(".views-field-title a"):
                continue
            meta = {
                "entity": response.meta["department_option"]["label"],
                "title": row.css(".views-field-title a::text").get().strip(),
                "category": row.css(".views-field-field-tender-category::text").get().strip(),
                "number": row.css(".views-field-field-code::text").get().strip(),
                "date_published": row.css(
                    ".views-field-field-date-published").xpath(".//span/@content").get(),
                "closing_date": row.css(
                    ".views-field-field-closing-date").xpath(".//span/@content").get(),
                "compulsory_briefing_date": row.css(
                    ".views-field-field-compulsory-briefing-sessio").xpath(".//span/@content").get(),
            }
            relative_url = row.css(".views-field-title").xpath(".//a/@href").get().strip()
            absolute_url = response.urljoin(relative_url)
            yield scrapy.http.Request(absolute_url, self.parse_tender, meta=meta)

    def create_search_request(self, department_option, page_number):
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
            "page": str(page_number),
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

    def parse_tender(self, response):
        overview_html = response.css(".field-name-field-econtact").get()
        overview_markdown = h.handle(overview_html)
        tender_item = EtenderItem(
            url=response.url,
            number=response.meta["number"],
            entity=response.meta["entity"],
            title=response.meta["title"],
            category=response.meta["category"],
            date_published=response.meta["date_published"],
            closing_time_and_date=response.meta["closing_date"],
            compulsory_briefing_session=response.meta["compulsory_briefing_date"],
            overview_markdown=overview_markdown,
            overview_html=overview_html,
        )
        yield tender_item

def get_select_options(field_name, response):
    field_option_elements = response.css(f"#edit-field-{field_name}-tid option")
    return [
        {
            "value": o.xpath("@value").get(),
            "label": o.xpath("text()").get(),
        }
        for o in field_option_elements
    ]
