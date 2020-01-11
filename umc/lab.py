import cfscrape
# from fake_useragent import UserAgent
from scrapy.http import Request
# ua = UserAgent()
# r_agent = ua.random
# #
# # proxies = {"http": "http://localhost:8080", "https": "http://localhost:8080"}
# # tokens, user_agent = cfscrape.get_tokens("http://moviespedia.net/", r_agent)
# # print(tokens)
# # import cfscrape
# # # scraper = cfscrape.create_scraper()
# import cloudscraper
# scraper = cloudscraper.create_scraper()
# result = scraper.get_tokens("https://w1.spacemov.cc/actor/serhii-averchenko/",)
# print(result)
# import urllib.request

# def returner():
#     new = fetch(url='https://hqq.tv/player/embed_player.php?vid=a2ZtNVRNMEJ2SCszNDJZckZIQ2k0QT09#iss=MTI0LjQxLjE5My4zMg==')
#     print(new)
#     return new
#
# a = returner()
# print(a)

# req = urllib.request.Request(url='https://hqq.tv/player/embed_player.php?vid=a2ZtNVRNMEJ2SCszNDJZckZIQ2k0QT09#iss=MTI0LjQxLjE5My4zMg==')
# print(req)

# import requests
#
# URL = 'https://hqq.tv/player/embed_player.php?vid=a2ZtNVRNMEJ2SCszNDJZckZIQ2k0QT09#iss=MTI0LjQxLjE5My4zMg=='
# # query = {'your': 'dictionary to send'}
#
# response = requests.post(URL)
# print(response.status_code)
from scrapy.loader import ItemLoader

from umc.items import UmcItem

z = list(range(10))
add_func = lambda z : z*2
n_z = list(map(add_func,z))
print(add_func)
print(z)
print(n_z)
#
# is_odd = lambda z: z % 2 == 1
# n_z = list(filter(is_odd,z))
# print(n_z)
#
# a,*b,c,d = z
# print(f'a={a},b={b},c={c},d={d}')
# import time
#
# start_time = time.time()
# # b = datetime.datetime.time()'
# result = time.localtime(start_time)
# print(start_time)
# print(result)
# from scrapy_splash import SplashRequest
#
# splash_args = {
#             'html': 1,
#             'png': 1,
#             'width': 600,
#             'render_all': 1,
#         }
#         fetch(SplashRequest(response.url, endpoint='render.html',
#                             args=splash_args))

import re
# url = 'https://vidcloud9.com/streaming.php?id=NDA3MzU=&title=Power+-+Season+1+Episode+01%3A+Not+Exactly+How+We+Planned&typesub=SUB&sub=L3Bvd2VyLXNlYXNvbi0xLWVwaXNvZGUtMDEtbm90LWV4YWN0bHktaG93LXdlLXBsYW5uZWQvcG93ZXItc2Vhc29uLTEtZXBpc29kZS0wMS1ub3QtZXhhY3RseS1ob3ctd2UtcGxhbm5lZC52dHQ=&cover=L3Bvd2VyLXNlYXNvbi0xLWF3dy9jb3Zlci5wbmc='
# a = re.findall(r"https://vidcloud9.com/streaming\.php\?id=([a-zA-Z0-9]+)", url)
# print(a)
# pattern = 'https://vidcloud9.com/streaming\.php\?id=[a-zA-Z0-9]+'
# a = pattern.replace('[','([').replace('+','+)')
# print(a)
pattern = r'r"//hindilinks4uto.com/player/embed_player.php\?vid=[a-zA-Z#=]+"'
a = re.sub(r'\[.*', '[a-zA-Z0-9]+"', pattern)
# a = r"//vidcloud9.com/load\.php\?id=([a-zA-Z0-9]+)"
print(pattern, a)


import scrapy
from scrapy.loader.processors import MapCompose, Join
a = Join(['hi','John'])
print(a)
b=[]
map(a,b)
print(b)
l = ItemLoader(item=UmcItem(), response=response.url)