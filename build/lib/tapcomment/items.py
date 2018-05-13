# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TapcommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    game_name = scrapy.Field()
    game_id = scrapy.Field()
    game_rate = scrapy.Field()
    comment_author = scrapy.Field()
    author_verified = scrapy.Field()
    author_id = scrapy.Field()
    comment_id = scrapy.Field()
    comment_rate = scrapy.Field()
    comment_time = scrapy.Field()
    comment_phone = scrapy.Field()
    comment_content = scrapy.Field()
    comment_smile = scrapy.Field()
    comment_up = scrapy.Field()
    comment_down = scrapy.Field()
    comment_reply = scrapy.Field()
    pass
