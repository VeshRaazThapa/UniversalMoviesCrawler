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
