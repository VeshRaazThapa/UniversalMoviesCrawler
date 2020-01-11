from collections import defaultdict

import cloudscraper

from umc.spiders.utils.importing_modules import *
from umc.spiders.utils.embed_domain_list import _not_detail_pages
headers = {
    'user_agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
}
splash_meta = {
    # 'args': {
    #     # set rendering arguments here
    #     'html': 1,
    #     'png': 0,
    #     'wait': 3,
    #     # 'url' is prefilled from request url
    #     # 'http_method' is set to 'POST' for POST requests
    #     # 'body' is set to request body for POST requests
    # },

    # optional parameters
    'endpoint': 'render.html',  # optional; default is render.json
    # 'splash_url': '<url>',  # optional; overrides SPLASH_URL
    # 'slot_policy': scrapy_splash.SlotPolicy.PER_DOMAIN,
    'headers': headers,  # optional; a dict with headers sent to Splash
    # 'dont_process_response': True,  # optional, default is False
    # 'dont_send_headers': True,  # optional, default is False
    # 'magic_response': False,  # optional, default is True
}

# rotating user_agent is used for below splash

def splashrequest(url, callback,wait, meta=''):

    ua = UserAgent()
    r_agent = ua.random
    headers = {
        'user_agent': r_agent
    }
    return SplashRequest(url,
                         args={'wait': wait},
                         endpoint='render.html',
                         headers=headers,
                         callback=callback,
                         meta={'dont_retry': True, 's_info': meta},
                                    )


def cloudfare_response_result(response):
    url = response.url
    ua = UserAgent()
    r_agent = ua.random
    token, agent = cfscrape.get_tokens(url, r_agent)
    pass

def get_cookies_from_cloudscraper(self,url):

    ua = UserAgent()
    r_agent = ua.random
    scraper = cloudscraper.create_scraper()
    token, agent = scraper.get_tokens(url)
    self.token = token
    self.agent = agent


def not_detailp_check(url):
    for _not_detail_page in _not_detail_pages:
        if re.match(_not_detail_page, url):
            return True

    return False

def instantiate_arguments(self,domain, bypass_cloudflare, type):

    self.type = type
    self.domain = domain
    self.bypass_cloudflare = bypass_cloudflare
    self.start_time = 0
    ua = UserAgent()
    self.r_agent = ua.random


websites = defaultdict(str)
websites["cmovies.tv"] = {
    "splash": False,
    "detail_page_pattern": r"\/film\/.*/watching\.html\?.*",
    "tags": [""]
}

websites["www.bolly2tolly.net"] = {
    "splash": False,
    "detail_page_pattern": r"\/\?trembed=.*"
}

websites["fmovies.to"] = {
    "splash": True,
    "detail_page_pattern": r"\/film\/.*"
}

# properties of hosts:: given default is title and poster is extractable and splash is not needed
class DefaultHost:
    def __init__(self):
        pass

    def __call__(self, *args, **kwargs):
        return {"splash": False, "title": True, "poster": True,"wait":1}



hosts = defaultdict(DefaultHost())
# here if poster or title couldnot be extracted then it is defined so that hte possible data error is avoided
# here splash is to be used in host or not is defined
# for bypassing cloudflare wait is set 6
# hosts["www.fmebed.com"] = {
#     "splash": False,
#     "title": True,
#     "poster":
# }
# hosts["vidohd.com"] = {
#     "splash": False,
#     "title": True
# }
hosts["linkshrink.online"] = {
    "splash": True,
    "title": True,
    "poster": True,
    "wait": 1

}
hosts["mixdrop.co"] = {
    "splash": True,
    "title": True,
    "poster": True,
    "wait": 1

}
hosts["api.hdv.fun"] = {
    "splash":False,
    "title":False,
    "poster":True,
    "wait": 1
}
hosts["vidoza.net"] = {
    "splash":False,
    "title": False,
    "poster":True,
    "wait": 1
}
hosts["vidia.tv"] = {

         "splash": False,
         "title": False,
         "poster": False,
         "wait":1
                }
hosts["gounlimited.to"] = {
        "splash":True,
        "title":True,
        "poster":True,
        "wait":1
}
hosts["prostream.to"] = {

    "splash": False,
    "title": True,
    "poster": False,
    "wait":1
}
hosts["www.fembed.com"] = {
    "splash": True,
    "title": True,
    "poster": True,
    "wait":1

}
hosts["upfiles.pro"] = {
    "splash": False,
    "title":False,
    "poster":True,
    "wait": 1
}
hosts["player.clipot.tv"] = {
    "splash": False,
    "title": False,
    "poster": True,
    "wait":1
}
hosts["vidcloud.co"] = {
    "splash": False,
    "title": True,
    "poster": False,
    "wait": 1
}
hosts["vidcloud9.com"] = {
    "splash": False,
    "title": True,
    "poster": True,
    "wait": 1
}

hosts["vev.red"] = {
    "splash": True,
    "title": True,
    "poster": False ,## gives a poster but not reachable link
    "wait":1
}
hosts["vidnode.net"] = {
    "splash": False,
    "title": True,
    "poster": False,
    "wait":1
}
hosts["cdn.123moviesapp.net"] = {
    "splash": True,
    "title": True,
    "poster": True,
    "wait":1
}
hosts["gcloud.live"] = {
    "splash": True,
    "title": True,
    "poster": True,
    "wait": 1
}
hosts["entervideo.net"] = {
    "splash": False,
    "title": False,
    "poster": True,
    "wait": 1
}
hosts["ok.ru"] = {
    "splash": False,
    "title": False,
    "poster": True,
    "wait": 1
}
hosts["moviemaniac.org"] = {
    "splash": True,
    "title": True,
    "poster": True,
    "wait": 1
}

hosts["onlystream.tv"] = {
    "splash":True,
    "title":True,
    "poster":True,
    "wait":6
}
hosts["nxload.com"] = {
    "splash":False,
    "title":False,
    "poster":True,
    "wait":1
}

hosts["ww.mp4upload.com"] = {
    "splash": True,
    "title": True,
    "poster": True,
    "wait": 1
}
hosts["vidsrc.me"] = {
    "splash": False,
    "title": False,
    "poster": True,
    "wait": 1
}