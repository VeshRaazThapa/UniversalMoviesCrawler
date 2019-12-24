import re

from scrapy.link import Link
from scrapy.linkextractors import LinkExtractor, IGNORED_EXTENSIONS
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.utils.misc import arg_to_iter
from scrapy.utils.python import unique
from scrapy.utils.url import url_has_any_extension, url_is_from_any_domain
from umc.spiders.utils.embed_domain_list import host_embed_patterns
import validators

url_pattern = r"((http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)"
# host_embed_patterns donot have https:,
# hostregexlinkExtractor extractacts link from below pattern and validates with host_embed_patterns to identify as a host
url_pattern_for_host = r"(//([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?)"
deny_extensions = {'.' + e for e in arg_to_iter(IGNORED_EXTENSIONS)}


def validator(link):
    for pattern in host_embed_patterns:
        find_result = re.findall(pattern, link)
        if len(find_result) > 0:
            return True
    return False


def x(x):
    return x


class HostRegexLinkExtractor(LinkExtractor):
    def __init__(self, pattern=url_pattern_for_host, process_value=x, *args, **kwargs):
        self.pattern = pattern
        self.process_value = process_value
        super(HostRegexLinkExtractor, self).__init__(*args, **kwargs)

    def extract_links(self, response):
        results = re.findall(self.pattern, response.text)
        links = list(filter(lambda x: "%s" not in x[0], results))
        links = list(map(lambda x: x[0], links))
        valid_links = list(filter(validator, links))
        valid_links = list(map(self.process_value, valid_links))
        valid_links = list(map(Link, valid_links))
        valid_links.extend(self._process_links(valid_links))
        return unique(valid_links)


class RegexLinkExtractor(LxmlLinkExtractor):
    def __init__(self, domain, *args, **kwargs):
        self.pattern = url_pattern
        self.domain = domain
        super(RegexLinkExtractor, self).__init__(*args,
                                                 **kwargs)

    def extract_links(self, response):
        results = re.findall(self.pattern, response.text)
        links = list(map(lambda x: x[0], results))
        links = list(filter(lambda x: url_is_from_any_domain(x, [self.domain]), links))
        links = list(filter(
            lambda x: not url_has_any_extension(x, deny_extensions), links
        )
        )
        links = list(map(Link, links))
        links.extend(self._process_links(links))
        return unique(links)
