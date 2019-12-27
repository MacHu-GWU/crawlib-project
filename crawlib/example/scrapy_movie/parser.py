# -*- coding: utf-8 -*-

from attrs_mate import attr, AttrsClass
import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from crawlib.status import Status
from . import items


class MovieListpageParseResult(scrapy.Item):
    page = scrapy



def parse_movie_listpage(html, current_listpage_id) -> scrapy.Item:
    item_list = list()
    now = datetime.now()

    soup = BeautifulSoup(html, "html.parser")


    movie_item_list = list()
    div_listpage = soup.find("div", id="listpage")  # type: BeautifulSoup
    for a in div_listpage.find_all("a"):
        href = a["href"]
        movie_id = href.split("/")[-1]
        movie_item = items.ScrapyMovieItem(
            _id=movie_id,
            title=None,
            status=Status.S50_Finished.id,
            edit_at=now,
        )
        movie_item_list.append(movie_item)

    div_pagination = soup.find("div", id="pagination")  # type: BeautifulSoup
    a_list = div_pagination.find_all("a")
    (
        a_previous_page,
        a_next_page,
        a_last_page,
    ) = a_list

    movie_listpage_item = items.ScrapyMovieListpageItem(
        _id=current_listpage_id,
        status=Status.S0_ToDo.id,
        edit_at=now,
    )
    item_list.append(movie_listpage_item)
    item_list.extend(movie_item_list)
    return item_list
