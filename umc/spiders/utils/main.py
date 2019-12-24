import re
from urllib.parse import urlparse
from urllib.parse import urlparse
from umc.constants import websites, hosts, splash_meta
from umc.spiders.utils.embed_domain_list import host_embed_patterns


def website_check(func):
    def wrapper(*args, **kwargs):
        domain = ""
        if websites[domain]:
            # execute func
            result = func(*args, **kwargs)
            return result
        else:
            raise Exception("Domain not in list")

    return wrapper


def get_splash_meta(domain):
    return splash_meta


def should_use_splash(domain, url):
    # TODO: implement condition for splash request
    return False
    return is_detail_page(domain, url)


def is_detail_page(domain, site):
    # is domain in list
    if websites[domain]:
        detail_page_pattern = websites[domain]["detail_page_pattern"]
        find_all = re.findall(detail_page_pattern, site)
        if is_empty(find_all):
            return False
        return True
    else:
        return False
        # raise Exception("Domain not in list")


def should_use_splash_for_detail_page(domain):
    return websites[domain]["splash"]


def should_use_splash_for_host(domain):
    # TODO: add host domain
    return False
    if hosts[domain]:
        return hosts[domain]["splash"]
    else:
        raise ("Host not found in list")


def is_empty(obj):
    if obj:
        if isinstance(obj, str):
            if obj != "":
                return False
        elif isinstance(obj, list):
            if len(obj) > 0:
                return False
        else:
            return True
    return True


def get_domain_from_url(url):
    return urlparse(url).netloc


def is_host_embed(url):
    for host_embed_pattern in host_embed_patterns:
        is_valid = len(re.findall(host_embed_pattern, url)) > 0
        if is_valid:
            return True
    return False

def clean_name(name):
    return name.replace('-', ' ')
