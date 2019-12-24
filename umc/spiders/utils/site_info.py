from umc.constants import websites
from umc.spiders.utils.main import get_domain_from_url
import re
from umc.spiders.utils.main import is_empty

def extractor(response):

    title = extract_title(response)
    link = response.url
    # TODO: check if tags is available and add tags
    return {"s_name": title, "site_link": link}

def extract_title(response):

    title = response.xpath("//title/text()").extract_first()
    if is_empty(title):
        title = url_title_extractor(response)
    # replacing domain from the url
    domain = get_domain_from_url(response.url)
    pattern = re.compile(domain, re.IGNORECASE)
    title = pattern.sub(domain, title.replace('-', ''))
    return title.replace(domain, '')


def url_title_extractor(response):
    site_url = response.url
    splits = site_url.split('/')
    title = max(splits, key=len)
    replace_texts = ['0123movies','.html','movie.pxqj']
    for replace_text in replace_texts:
        title.replace(replace_text, '')

    return title.replace('-', ' ')

