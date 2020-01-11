# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class UmcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # define the fields for your item here like:
    # name = scrapy.Field()
    i_description = Field()
    i_title = Field()
    s_i_images = Field()
    s_i_link = Field()
    s_id = Field()
    s_i_id = Field()
    size = Field()
    s_i_type = Field()  # tv shows , movie
    s_i_quality = Field()
    s_i_title = Field()
    embed_link = Field()
    file_link = Field()
    s_i_poster = Field()
    host_id = Field()
    created_date = Field()
    completor = Field()
    s_e_no = Field()
    h_i_quality = Field()
    s_a_quality = Field()
    release_date = Field()
    episode_title = Field()
    h_i_title = Field()
    h_i_size = Field()
    h_i_poster = Field()
    is_broken = Field()
    _id = Field()
    filecheck_na = Field()
    adult_content = Field()
    _id = Field()
