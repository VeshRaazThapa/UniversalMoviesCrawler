from umc.items import UmcItem

def parse_hostsite(response):

    item = UmcItem()
    # file_check = response.xpath('//*[@class="lead"]/text()').extract_first()
    item['embed_link'] = response.url
    h_i_title = response.xpath('//title/text()').extract_first()
    # if not h_i_title:
    #     h_i_title =
    item['h_i_title'] = h_i_title
    item['h_i_poster'] = response.xpath('//@poster').extract_first()

