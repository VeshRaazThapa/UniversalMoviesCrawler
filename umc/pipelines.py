# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import PTN
from process_data_vicaaya.Stream.MovieStream import MovieStream
from process_data_vicaaya.Stream.TvStream import TvStream
from process_data_vicaaya import utils
from umc.spiders.utils.main import *

is_movie_key = "is_movie"


def replace_from_str(text, replace_list):
    # replace_list = [("this", "that")]
    for item in replace_list:
        text.replace(item[0], item[1])
    return text


def has_season_or_episode(s_e_no):
    s_e_no = utils.dict_2_default_dict(s_e_no)
    return s_e_no and (s_e_no["episode"] or s_e_no["season"])


class UmcPipeline(object):
    def process_item(self, item, spider):
        return utils.dict_2_default_dict(item)


class MovieOrTv(object):
    def process_item(self, item, spider):
        # TODO: parse episode, season from host name or site name or site link
        # if no episode no. or sesaon episode no. it is Movie, else TV show
        # if TV show, item["is_movie"]: False else Tr

        h_name = item["h_name"]
        s_name = item["s_name"]
        s_link = item["s_link"]
        replacers = [("/", " "), ("?", " "), ("ep=", "episode"), ("-", " ")]
        parse = PTN.parse
        check = has_season_or_episode
        item[is_movie_key] = False
        item['stream_type'] = 'tv-show'
        if h_name and check(parse(h_name)):
            item['s_e_no'] = parse(clean_name(h_name))
        elif s_name and check(parse(s_name)):
            item['s_e_no'] = parse(clean_name(s_name))
        elif s_link and parse(s_link):
            formatted_s_link = replace_from_str(s_link, replacers)
            item['s_e_no'] = parse(formatted_s_link)
        else:
            item[is_movie_key] = True
            item['stream_type'] = 'movie'
        if not item[is_movie_key]:
            item["s_e_no"] = utils.dict_2_default_dict(item["s_e_no"])
        return item


class PostProcess(object):

    def process_item(self, item, spider):
        is_movie = item[is_movie_key]
        if is_movie:
            movie_item = MovieStream(item)
            return movie_item.get_data()
        else:
            tv_item = TvStream(item)
            return tv_item.get_data()
