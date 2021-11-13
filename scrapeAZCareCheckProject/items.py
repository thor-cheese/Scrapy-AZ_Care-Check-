# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import MapCompose, TakeFirst
from datetime import datetime







class ScrapeazcarecheckprojectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field(
        output_processor=TakeFirst()
        )

    address = Field(
        output_processor=TakeFirst()
        )

    city_state = Field(
        output_processor=TakeFirst()
        )

    facility_type = Field(
        output_processor=TakeFirst()
        )

    survey_date = Field(
        output_processor=TakeFirst()
        )
# str.strip
    survey_description = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )


class Scrapeazcarecheckproject_enforcement_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    name = Field(
        output_processor=TakeFirst()
        )
    address = Field(
        output_processor=TakeFirst()
        )

    city_state = Field(
        output_processor=TakeFirst()
        )

    facility_type = Field(
        output_processor=TakeFirst()
        )
    license = Field(
        output_processor=TakeFirst()
        )

    address_from_page = Field(
        output_processor=TakeFirst()
        )

    name_from_page = Field(
        output_processor=TakeFirst()
        )

    enforcement_date = Field(
        output_processor=TakeFirst()
        )

    civil_penalty = Field(
        output_processor=TakeFirst()
        )
# str.strip
    enforcement_description = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
        )


class Count_Facilities_Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field(
        output_processor=TakeFirst()
        )

    address = Field(
        output_processor=TakeFirst()
        )

    city_state = Field(
        output_processor=TakeFirst()
        )

    facility_type = Field(
        output_processor=TakeFirst()
        )
