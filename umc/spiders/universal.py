# -*- coding: utf-8 -*-
from checkhost.main import check_host
from scrapy.cmdline import execute
from umc.spiders.utils.RegexLinkExtractor import HostRegexLinkExtractor, RegexLinkExtractor
from umc.spiders.utils.embed_domain_list import host_domain_list
from umc.spiders.embedlink_parser import *
from umc.spiders.utils.main import *
from umc.spiders.utils.site_info import extractor
from umc.constants import *
import time
import logging


cfscrape.DEFAULT_CIPHERS = 'TLS_AES_256_GCM_SHA384:ECDHE-ECDSA-AES256-SHA384'


class HomeScraperSpider(CrawlSpider):
    handle_httpstatus_list = [429, 503]
    name = 'universal'

    def __init__(self, domain, bypass_cloudflare=False, type='all', *args, **kwargs):

        instantiate_arguments(self,domain, bypass_cloudflare, type)
        """cloud flare using sites are listed in locally hosted page to use cloudscraper in starturl"""
        home_url = 'https://%s' % domain
        cloudflare_using_sites = 'file:///Users/stuff/Desktop/embed_test.html'

        if type == 'all':
            if self.bypass_cloudflare:
                self.start_time = time.time()
                get_cookies_from_cloudscraper(self, home_url)
                self.start_urls = [cloudflare_using_sites]
            else:
                self.start_urls = \
                    [home_url]
            """selects all the links having same domain as the site"""
            allowed_domains: str = self.domain
            self.rules = (
                Rule(LinkExtractor(allow_domains=allowed_domains, deny_domains=host_domain_list,
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
                                   attrs=('href', 'player-data', 'data-video', 'src', 'data-vs'),
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
        s_info = ''
        # meta = {}
        # if should_use_splash(self.domain, url):
        #     meta = {**meta, 'splash': get_splash_meta(self.domain)}
        #     print("using splash request")
        #     return SplashRequest(response.url, **splash_meta)
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
        # provides embedlinks but are not detailpage we needed
        if not_detailp_check(url):
                s_info = extractor(response)
        # scraping all the cloudflare protected links
        if self.bypass_cloudflare :
            """getting new token in 15 min interval"""
            if (time.time() - self.start_time) >= 900:
                logging.info("15 min passed.....getting new token")
                get_cookies_from_cloudscraper(self, url)
                self.start_time = time.time()

            return Request(url=url, cookies=self.token,
                           headers={'User-Agent': self.agent},
                           meta={'s_info': s_info, 'dont_retry': True})
        return Request(url=url, headers={'User-Agent': self.r_agent},
                       meta={'s_info': s_info,
                             'don_retry': True})

    def process_request_host(self, request, response):
        """request==embedlink,response=site_link"""

        url = request.url
        s_info = extractor(response)
        if 'https:' not in url and 'http:' not in url:
            url = response.urljoin(url)
        if not_detailp_check(response.url):
            s_info = response.meta.get('s_info')
        domain = get_domain_from_url(url)
        if is_host_embed(self, url):
            s_info.update({'_id': self._id})# is is_host_embed then _id is instantiated
            if hosts[domain]["splash"]:
                wait = hosts[domain]["wait"]
                return splashrequest(url, self.process_embed, wait, s_info)
            else:
                return Request(url, callback=self.process_embed,
                               headers={'User-Agent': self.r_agent},
                               meta={'s_info': s_info})
        else:
            return Request(url, headers={'User-Agent': self.r_agent},
                           meta={'s_info': s_info})

    def process_embed(self, response):
            logging.info("embed link found : %s" % response.url)
            domain = get_domain_from_url(response.url)
            broken_dict = check_host(response)
            if not broken_dict["broken"]:
                poster = None
                title = None
                if hosts[domain]["poster"]:
                    poster = poster_parser(response)
                if hosts[domain]["title"]:
                    title = title_parser(response)
                return {"embed_link": response.url,
                        "poster": poster,
                        "h_name": title,
                        "new": True,
                        **response.meta['s_info']}


if __name__ == "__main__":
    execute('scrapy crawl universal -a domain =moviespedia.net'.split())