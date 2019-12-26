# -*- coding: utf-8 -*-

import pytest
import requests

from crawlib.example.scrapy_movie import parser


def test():
    html = requests.get("http://127.0.0.1:58461/movie/listpage/1").text
    result = parser.parse_movie_listpage(html, current_listpage_id=1)
    assert isinstance(result[0], parser.items.ScrapyMovieListpageItem)
    for item in result[1:]:
        assert isinstance(item, parser.items.ScrapyMovieItem)



if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
