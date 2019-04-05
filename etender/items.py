# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EtenderItem(scrapy.Item):
    url = scrapy.Field()
    number = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    slug = scrapy.Field()
    date_published = scrapy.Field()
    closing_time_and_date = scrapy.Field()
    compulsory_briefing_session = scrapy.Field()
    institution = scrapy.Field()
    delivery_location = scrapy.Field()
    enquiries = scrapy.Field()
    contact_person = scrapy.Field()
    contact_email = scrapy.Field()
    contact_telephone = scrapy.Field()
    contact_fax = scrapy.Field()
    bid_docs_website = scrapy.Field()
    bid_docs_physical_address = scrapy.Field()
    bid_delivery_physical_address = scrapy.Field()
    briefing_date = scrapy.Field()
    briefing_time = scrapy.Field()
    briefing_venue = scrapy.Field()
    special_conditions = scrapy.Field()

class FileItem(scrapy.Item):
    tender_url = scrapy.Field()
    name = scrapy.Field()
    file_urls = scrapy.Field()
