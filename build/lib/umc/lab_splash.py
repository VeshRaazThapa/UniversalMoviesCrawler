1. docker run -d -p 8050:8050 --memory=4.5G --restart=always scrapinghub/splash:3.1 --maxrss 4000
2. curl 'http://localhost:curl 'http://localhost:8050/render.html?url=%%&timeout=10&wait=0.5'
3. fetch(SplashRequest(response.url,args={'wait': 1},endpoint='render.html',headers={'user_agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Mobile Safari/537.36'},dont_filter=True))

###
from scrapy_splash import SplashRequest
url='https://database.gdriveplayer.us/player.php?type=anime&id=108&episode=38'
args={'wait': 2, 'width': 320, 'timeout': 60, 'render_all': 1}
headers={'user_agent': 'Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Mobile Safari/537.36'}
endpoint='render.html'
sr=SplashRequest(url=url, args=args, endpoint=endpoint,headers=headers)
fetch(sr)




5 15:50:13.926733 [events] {"active": 0, "timestamp": 1579103413, "maxrss": 278184, "rendertime": 6.8601179122924805, "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "args": {"timeout": 60, "headers": {"Accept-Language": "en", "User_Agent": "Mozilla/5.0 (Linux; Android 8.0.0; Pixel 2 XL Build/OPD1.170816.004) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Mobile Safari/537.36", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}, "url": "https://database.gdriveplayer.us/player.php?type=anime&id=108&episode=38", "wait": 2, "render_all": 1, "width": 320, "uid": 139716176405168}, "status_code": 200, "client_ip": "172.17.0.1", "load": [0.06, 0.13, 0.1], "path": "/render.html", "qsize": 0, "method": "POST", "fds": 38, "_id": 139716176405168}
2020-01-15 15:50:13.929823 [-] "172.17.0.1" - - [15/Jan/2020:15:50:13 +0000] "POST /render.html HTTP/1.1" 200 152340 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"
