# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EtenderItem(scrapy.Item):
    url = scrapy.Field()
    number = scrapy.Field()
    description_short = scrapy.Field()
    category = scrapy.Field()
    date_published = scrapy.Field()
    closing_time_and_date = scrapy.Field()
    compulsory_briefing_session = scrapy.Field()
    free_text = scrapy.Field()


class FileItem(scrapy.Item):
    tender_url = scrapy.Field()
    name = scrapy.Field()
    file_urls = scrapy.Field()
