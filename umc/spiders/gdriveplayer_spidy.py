# -*- coding: utf-8 -*-
import scrapy
from umc.spiders.utils.importing_modules import *
from umc.spiders.embedlink_parser import *
from checkhost.main import check_host
from umc.constants import *

class GdriveplayerSpidySpider(scrapy.Spider):
    name = 'gdriveplayer_spidy'
    allowed_domains = ['database.gdriveplayer.us']

    def __init__(self, type='all',domain='', **kwargs):
        self.type = type
        if self.type == 'all':
            self.start_urls = ['https://database.gdriveplayer.us/movie.php',
                               'https://database.gdriveplayer.us/anime.php',
                               'https://database.gdriveplayer.us/drama.php',
                               'https://database.gdriveplayer.us/series.php']

        else:
            self.start_urls = ['%s' % domain]

        super().__init__()

    def parse(self, response):
        if self.type == 'daily' or 'movie.php' in response.url:
            yield Request(response.url,callback=self.movie_link_parser,dont_filter=True)
        else:
            item_links = response.xpath('//td//@href').extract()
            for link in item_links:
                if 'series.php' in link or 'anime.php' in link or 'drama.php' in link:
                    yield Request(response.urljoin(link), callback=self.movie_link_parser)
        next_pages = response.xpath('//*[@class="pagination"]/a/@href').extract()
        if self.type == 'all':
            for next_page in next_pages:
                yield Request(response.urljoin(next_page), callback=self.parse)

    def movie_link_parser(self, response):
        s_i_link = response.url
        embed_links = re.findall(r'player.php\?[0-9a-zA-Z&=?]+', response.text)
        for embed_link in embed_links:
            # s_i_title = response.xpath("//*[@href='%s']/text()" % embed_link).extract_first()
            if 'movie.php' in response.url or self.type == 'daily':
                s_i_link = response.xpath("//*[contains(@href,'%s')]/../../../td[3]/b/a/@href" % embed_link).extract_first()

            s_info = {"s_name": None, "site_link": response.urljoin(s_i_link)}
            # yield Request(response.urljoin(embed_link), callback=self.embedlink_parser, meta={'s_info': s_info})
            wait = 2
            # yield splashrequest(response.urljoin(embed_link), self.embedlink_parser, wait, s_info)
            yield SplashRequest(
                         response.urljoin(embed_link),
                         args={'wait': wait,
                               'timeout': 90,
                               },
                         endpoint='render.html',
                         headers=headers,
                         dont_send_headers=True,
                         callback=self.embedlink_parser,
                         meta={'dont_retry': True, 's_info': s_info},
                                    )

    def embedlink_parser(self, response):
        broken_dict = check_host(response)
        if not broken_dict["broken"]:
            embed_link = response.url
            h_i_title = response.xpath('//title/text()').extract_first()
            poster = poster_parser(response)

            return {"embed_link": embed_link,
                    "poster": poster,
                    "h_name": h_i_title,
                    "new": True,
                    **response.meta['s_info']}




