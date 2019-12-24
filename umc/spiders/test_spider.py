# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy_splash import SplashRequest
from scrapy.cmdline import execute
from umc.spiders import embedlink_parser

from umc.constants import headers, splash_meta
from umc.spiders.utils.embed_domain_list import host_domain_list
from umc.spiders.embedlink_parser import *
from umc.spiders.utils.main import *


class HomeScraperSpider(Spider):
    handle_httpstatus_list = [301, 302]

    name = 'test_spider'
    start_urls = [
        'https://mixdrop.co/e/9kpzmidj'
    ]

    def parse(self, response):
        return SplashRequest(response.url,
                             args={'wait': 1},
                             endpoint='render.html',
                             headers={'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'},
                             callback=self.again)

    def again(self, response):
        poster = poster_parser(response)
        title = title_parser(response)
        return {'h_poster':poster,'h_title':title}



if __name__ == "__main__":
    execute('scrapy crawl test_spider'.split())
