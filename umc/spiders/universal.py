# -*- coding: utf-8 -*-
from scrapy.cmdline import execute
from umc.spiders.utils.RegexLinkExtractor import HostRegexLinkExtractor, RegexLinkExtractor
from umc.spiders.utils.embed_domain_list import host_domain_list, host_embed_patterns,_not_detail_pages
from umc.spiders.embedlink_parser import *
from umc.spiders.utils.main import *
from umc.spiders.utils.site_info import extractor
from umc.spiders.utils.check_host import *
from umc.constants import *
import time

cfscrape.DEFAULT_CIPHERS = 'TLS_AES_256_GCM_SHA384:ECDHE-ECDSA-AES256-SHA384'


class HomeScraperSpider(CrawlSpider):
    handle_httpstatus_list = [429]

    name = 'universal'

    def __init__(self, domain, use_cloudfare=False, type='all', *args, **kwargs):
        self.type = type
        self.domain = domain
        self.use_cloudfare = use_cloudfare
        ua = UserAgent()
        self.r_agent = ua.random
        if type == 'all':
            self.start_urls = \
                ['https://%s' % domain]
            # self.start_urls = ['https://www5.series9.to/film/ncis-los-angeles-season-6-hzd/watching.html']
            # self.start_urls = ['https://m.genvideos.io/watch_6_Balloons_2018.html']
            # self.start_urls = ['https://hdbest.net/city-of-ghosts-2017-206.html']
            # self.start_urls = ['https://www.bolly2tolly.net/movie/odu-raja-odu-2018-hd']
            # self.start_urls = ['http://nites.tv/movies/portrait-of-a-lady-on-fire/']
            ##selects all the links having same domain as the site

            allowed_domains: str = self.domain
            self.rules = (
                Rule(LinkExtractor(allow_domains=allowed_domains, deny_domains=(),
                                   tags=('iframe', 'li', 'area', 'a'),
                                   attrs=('href', 'player-data', 'data-video', 'src')),
                     # follow=True,
                     process_request='process_request'
                     ),
                # extracts all the links having the site domain from response.text
                Rule(RegexLinkExtractor(domain=allowed_domains),
                     # follow=True,
                     process_request='process_request'),
                Rule(LinkExtractor(allow_domains=host_domain_list, deny_domains=(),
                                   tags=('a', 'area', 'li', 'iframe'),
                                   attrs=('href', 'player-data', 'data-video', 'src'),
                                   # restrict_text=host_embed_patterns,
                                   # process_value=self.process_embed_link
                                   ),
                     follow=False,
                     process_request='process_request_host',
                     # callback='process_embed'
                     ),
                # extracts links matching host regex in the response.text and callbacks
                Rule(
                    HostRegexLinkExtractor(process_value=lambda x: "https:" + x),
                    process_request='process_request_host',
                    # callback='process_embed'
                )
            )

        super().__init__()

    def process_request(self, request, response):
        url = request.url
        meta = {}
        s_info = ''
        if should_use_splash(self.domain, url):
            meta = {**meta, 'splash': get_splash_meta(self.domain)}
            print("using splash request")
            return SplashRequest(response.url, **splash_meta)
        # this is for website having same domain for website and host as well eg. afdah.info
        # splasRequest to bypass cloudfare
        # if is_host_embed(url):
        #         s_info = extractor(response)
        #         return SplashRequest(request.url,
        #                              args={'wait': 1},
        #                              **splash_meta,
        #                              callback=self.process_embed,
        #                              meta={'dont_retry': True, 's_info': s_info},
        #                              )
        # provides embedlinks but are not detailpage
        if not_detailp_check(url):
                s_info = extractor(response)
        # scraping all the cloudfare protected links with cfscrape
        # TODO: to use cfscrape for the  starturls

        if self.use_cloudfare:
            token, agent = cfscrape.get_tokens(url, self.r_agent)
            return Request(url=url, cookies=token, headers={'User-Agent': agent}, meta={'dont_retry': True})

        return Request(url=url, headers={'User-Agent': self.r_agent}, meta={'dont_retry': True, 's_info': s_info})

    def process_request_host(self, request, response):
        # TODO: check whether to use splash
        # TODO: extract info form site page
        # request==embedlink,response=site_link
        url = request.url
        if 'https:' not in url and 'http:' not in url:
            url = response.urljoin(url)
        s_info = extractor(response)
        if not_detailp_check(response.url):
            s_info = response.meta.get('s_info')
        domain = get_domain_from_url(url)
        if is_host_embed(url):
            if hosts[domain]["splash"]:
                wait = hosts[domain]["wait"]
                return splashrequest(url, self.process_embed, wait, s_info)
            else:
                return Request(url, callback=self.process_embed, headers={'User-Agent': self.r_agent}, meta={'dont_retry': True, 's_info': s_info})
        else:
            return Request(url, headers={'User-Agent': self.r_agent}, meta={'dont_retry': True, 's_info': s_info})

    def process_embed(self, response):
        # if is_host_embed(response.url):
            # specially for maniac.org host
            if response.status == 429 or '429 Too Many Requests' in response.text:
                time.sleep(40)
                wait = 1
                s_info = response.meta['s_info']
                return splashrequest(response.url, self.process_embed, wait, s_info)

            print("embed link found : ", response.url)
            domain = get_domain_from_url(response.url)
            broken_dict = check_host(response)
            if not broken_dict["broken"]:
                poster = None
                title = None
                if hosts[domain]["poster"]:
                    poster = poster_parser(response)
                if hosts[domain]["title"]:
                    title = title_parser(response)
                return {"embed_link": response.url, "poster": poster, "h_name": title, "new": True, **response.meta['s_info']}


if __name__ == "__main__":
    execute('scrapy crawl universal -a domain=vmovie.biz'.split())