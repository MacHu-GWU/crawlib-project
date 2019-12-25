# -*- coding: utf-8 -*-

import scrapy

class MovieSpider(scrapy.Spider):
    name = "movie"

    def start_requests(self):
        urls = [
            "http://127.0.0.1:58461/movie/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

