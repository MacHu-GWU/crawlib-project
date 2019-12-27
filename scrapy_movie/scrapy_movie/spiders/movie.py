# -*- coding: utf-8 -*-

import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from crawlib.status import Status
from crawlib.example.scrapy_movie import (
    config, items, parser
)
from crawlib.example.scrapy_movie.url_builder import url_builder


class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        listpage_id_list = [
            1,
        ]
        for listpage_id in listpage_id_list:
            url = url_builder.listpage_url(listpage_id)
            yield scrapy.Request(
                url=url,
                callback=self.parse_movie_listpage,
                meta={"listpage_id": listpage_id}
            )

    def parse_movie_listpage(self, response):
        result = parser.parse_movie_listpage(
            response.text,
            current_listpage_id=response.meta["listpage_id"]
        )
        for item in result:
            item.process()
            # yield item
