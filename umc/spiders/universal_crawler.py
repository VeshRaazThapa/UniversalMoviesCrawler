# -*- coding: utf-8 -*-
from scrapy_splash import SplashRequest
from scrapy.cmdline import execute

from umc.constants import headers, splash_meta
from umc.spiders.utils.embed_domain_list import host_domain_list
from umc.spiders.embedlink_parser import *
from umc.spiders.utils.main import *


class HomeScraperSpider(CrawlSpider):
    handle_httpstatus_list = [301, 302]

    name = 'universal_crawler'

    def __init__(self, domain, type='all', *args, **kwargs):
        self.type = type
        self.domain = domain
        if type == 'all':
            self.start_urls = ['https://%s/' % domain]
            self.rules = (
                Rule(LinkExtractor(allow_domains=domain, deny_domains=host_domain_list,
                                   tags=('a', 'area', 'li', 'iframe'),
                                   attrs=('href', 'player-data', 'data-video', 'src')),
                     follow=True,
                     callback='print_splash_response',
                     process_request='process_request'
                     ),
                Rule(LinkExtractor(allow_domains=host_domain_list, deny_domains=(),
                                   tags=('a', 'area', 'li', 'iframe'),
                                   attrs=('href', 'player-data', 'data-video', 'src'),
                                   # process_value=self.process_embed_link
                                   ),
                     process_request='process_request_host',
                     callback='process_embed'
                     )
            )

        super().__init__()

    def process_request(self, request, response):
        url = request.url
        meta = {}
        if should_use_splash(self.domain, url):
            meta = {**meta, 'splash': get_splash_meta(self.domain)}
            return SplashRequest(response.url, **splash_meta)
        return Request(url=url)

    def process_request_host(self, request, response):
        # TODO: check whether to use splash

        return Request(url=request.url)

    def print_splash_response(self, response):
        splash_meta = response.meta["splash"]
        if splash_meta:
            print("Response : ", response)
        return response

    def page_check(self, response):
        """
        checks if page is detail page or not
        :param response:
        :return:
        """

        if is_detail_page(self.domain, response.url):
            print("Detail page found")
            if should_use_splash_for_detail_page(self.domain):
                print("using splash request for detail page")
                yield SplashRequest(response.url,
                                    args={'wait': 3, 'html': 1, 'png': 0},
                                    endpoint='render.html',
                                    headers=headers,
                                    callback=self.extract_embed_links)
            else:
                return self.extract_embed_links(response)
        else:
            return self.extract_embed_links(response)

    def process(self):
        # TODO: extract all links, filter embed links, request other links
        pass

    @staticmethod
    def extract_all_links(response):
        # TODO: extract all links
        pass

    def extract_embed_links(self, response):
        # TODO: use regex to find all the links from the page
        # TODO: filter hosts
        print("Extracting embed link")
        data_links = response.xpath("//li/@data-video").extract()
        player_data_links = response.xpath("//*/@player-data").extract()
        links = response.xpath("//a/@href").extract()
        links_iframe = response.xpath("//iframe/@src").extract()
        final_links = [*data_links, *links_iframe, *player_data_links, *links]
        print("Final links : ", final_links)
        for link in final_links:
            yield self.process_embed_link(link)
        # LinkExtractor(allow_domains=(host_domain_list), deny_domains=(), tags=('a', 'area', 'li', 'iframe'),
        #                    attrs=('href', 'player-data', 'data-video', 'src'), process_value=self.process_embed_link)

    def process_embed(self, response):
        return {"embed_link": response.url}

    def process_embed_link(self, link):
        # TODO: complete incomplete links
        # process links
        # link = link.replace("//", "")
        print("Embed link : ", link)
        if not "https" in link and "vidnode" in link:
            link = "https:" + link
        host_domain = get_domain_from_url(link)
        if should_use_splash_for_host(host_domain):
            yield SplashRequest(link, args={'wait': 1}, endpoint='render.html', headers=headers,
                                callback=self.inner_page)
        else:
            yield Request(url=link, callback=self.inner_page)

    def inner_page(self, response):
        item = UmcItem()

        # s_i_link = ''
        # item['s_i_link'] = s_i_link
        # item['s_i_title'] = s_i_link.split('/')[-2].replace('-', ' ')
        # pattern = re.compile(r'\/(movies?|series?|tv-shows?)\/', re.IGNORECASE)
        # match = re.findall(pattern, s_i_link)
        # match = list(map(lambda x: x.lower(), match))
        # if 'serie' in match or 'tv-show' in match or 'series' in match:
        # if 'serie' in match or 'tv-show' in match or 'series' in match:
        #     item['s_i_type'] = 'tv-show'
        # else:
        #     item['s_i_type'] = 'movie'
        h_i_poster = poster_parser(response)
        if h_i_poster and len(h_i_poster > 1):
            item['h_i_poster'] = response.urljoin(h_i_poster[0])
        # h_i_title =
        # with open("umc/spiders/utils/hosts_list.json") as json_file:
        #     datas = json.load(json_file)
        #     for data in datas:
        #         if host_domain in data:
        #             format = data[host_domain]
        #             embed_link = format + response.url.split('/')[-1]
        #         else:
        #             embed_link = response.url
        item['embed_link'] = response.url
        return item


if __name__ == "__main__":
    execute('scrapy crawl universal_crawler -a domain=fmovies.to'.split())
