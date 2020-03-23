# -*- coding: utf-8 -*-
from umc.spiders.utils.importing_modules import *

def poster_parser(response):
    custom_check = custom_host_poster_extract(response)
    ## for individual hosts
    if custom_check['bool']:
        return custom_check['poster']
    poster_url_extract = response.xpath('//@poster').extract_first()
    # https://www.fembed.com/v/vstr><div style=padding-left:56.25%;>
    # </div><div style=top:0;left:0;bottom:0;right:0;width:100%;height:100%;position:absolute;background:#000 no-repeat 50% 50%;background-size:contain
    # ;background-image:url(/asset/userdata/225754/player/3769_poster.png?v=1558635221);
    if not poster_url_extract or len(poster_url_extract) < 4: # above xpath may just give |
        # test_poster_urls = re.findall(r'\((.*)\)', response.text)
        ## select all the character between () and without (
        test_poster_urls = re.findall(r'(?<=\()[^(]+(?=\))', response.text)
        poster_url_extract = poster_url_extracter(test_poster_urls, response)

    # is has ' in the regex result below than the poster_url is ' this.jpg|png'
    if not poster_url_extract:
        # test_poster_urls = re.findall(r'\"(.*)\"', response.text)
        test_poster_urls = re.findall(r'(?<=\")[^\"]+(?=\")', response.text)
        poster_url_extract = poster_url_extracter(test_poster_urls, response)

    if not poster_url_extract:
        # test_poster_urls = re.findall(r'\'(.*)\'', response.text)
        # test_poster_urls = response.text.split('\'')
        test_poster_urls = re.findall(r'(?<=\')[^\']+(?=\')', response.text)
        poster_url_extract = poster_url_extracter(test_poster_urls, response)
    if poster_url_extract:
            poster_url_extract = response.urljoin(poster_url_extract)
    return poster_url_extract

def custom_host_poster_extract(response):

    if 'ok.ru' in response.url:
        poster = response.xpath('//img/@src').extract_first()
        return {"poster":poster,"bool": True}
    return {"poster": None, "bool": False}



def poster_url_extracter(test_poster_urls,response):

    poster_url_extract = None
    for test_poster_url in test_poster_urls:
        ## priority is given to .jpg as it has high chance of being poster over .png
        if '.jpg' in test_poster_url:
            raw_poster_url = response.urljoin(test_poster_url).replace('\\', '')
            if is_poster_valid(raw_poster_url):
                poster_url_extract = raw_poster_url
                return poster_url_extract
    for test_poster_url in test_poster_urls:
        ## priority is given to .jpg as it has high chance of being poster over .png
        if '.jpeg' in test_poster_url:
            raw_poster_url = response.urljoin(test_poster_url.replace('\\',''))
            if is_poster_valid(raw_poster_url):
                poster_url_extract = raw_poster_url
                return poster_url_extract

    for test_poster_url in test_poster_urls:
        if '.png' in test_poster_url:
            raw_poster_url = response.urljoin(test_poster_url.replace('\\', ''))
            if is_poster_valid(raw_poster_url):
                poster_url_extract = raw_poster_url
    return poster_url_extract


def is_poster_valid(poster_url_extract):

    invalid_symbols = ['<', '>', '{', ';', '.js', 'adblock', '"', '\'', 'dablock','falcon', 'logo.png','favicon.png','icon.png']
    for invalid_symbol in invalid_symbols:
        if invalid_symbol in poster_url_extract:
            return False

    return True


def title_parser(response):
    title = response.xpath('//title/text()').extract_first()
    if not title:
        title = response.xpath('//*[@itemprop="name"]/text()').extract_first()
    if not title:
        title = response.xpath('//*[@class="title"]//text()').extract_first()

    return title
