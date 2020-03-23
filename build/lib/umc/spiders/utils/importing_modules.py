import scrapy
import json
import datetime
import re
from scrapy.http import Request
from scrapy.http import FormRequest
from scrapy.http import HtmlResponse
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from copy import deepcopy
from umc.items import UmcItem
from fake_useragent import UserAgent
from scrapy_splash import SplashRequest
import cfscrape
