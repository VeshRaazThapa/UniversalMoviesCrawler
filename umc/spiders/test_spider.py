# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.loader import ItemLoader
from scrapy_splash import SplashRequest
from scrapy.cmdline import execute
from umc.spiders import embedlink_parser

from umc.constants import headers, splash_meta
from umc.spiders.utils.embed_domain_list import host_domain_list
from umc.spiders.embedlink_parser import *
from umc.spiders.utils.main import *


class HomeScraperSpider(Spider):
    handle_httpstatus_list = [301, 302,503]

    name = 'test_spider'
    start_urls = [
        'https://www.fembed.com/v/5dr6xfdq14jw-zq#caption=https://sub.movie-series.net/joker/joker.vtt'
    ]

    def parse(self, response):
        yield Request(url=response.url, callback=self.again, meta={
            'donot_retry': True,'dont_filter':True

        })

    def again(self, response):
        # poster = poster_parser(response)
        # title = title_parser(response)
        # return {'h_poster':poster,'h_title':title}
        from scrapy.loader.processors import MapCompose, Join
        # a = Join(['hi', 'John'])
        # print(a)
        # b = []
        # map(a, b)
        # print(b)
        a = getattr(self, 'arg', 'asdf')
        print(a)
        l = ItemLoader(item=UmcItem(), response=response)
        l.add_xpath('h_i_title', '//title/text()', MapCompose(str.strip,str.title))
        return l.load_item()

if __name__ == "__main__":
    execute('scrapy crawl test_spider'.split())
