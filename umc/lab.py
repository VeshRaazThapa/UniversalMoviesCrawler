from umc.spiders.utils.check_host import *
u = 'https://video66.org/embed.php?w=745&h=450&vid=vids4/joy_of_life_-_02_clip1.mp4'

import urllib.request
f = urllib.request.urlopen(u)
content = f.content()
for black_word in blacklist_words:
    if black_word.lower() in content:
        is_broken = True
        print(is_broken, black_word)
