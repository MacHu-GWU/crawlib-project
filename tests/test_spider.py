#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pytest
from crawlib import exc
from crawlib.spider import get_domain_name, spider


def test_get_domain_name():
    url = "https://www.python.org/doc/"
    assert get_domain_name(url) == "www.python.org"
    

def test_get_html():
    url = "https://www.python.org/"
    html = spider.get_html(url)
    sys.stderr.write(html)


def test_download():
    url = "https://www.python.org/static/img/python-logo.png"
    dst = "python-logo.png"
    
    with pytest.raises(exc.NotDownloadError):
        spider.download(url, dst, minimal_size=1024*1024) # will not download
    assert os.path.exists(dst) is False
    
    with pytest.raises(exc.NotDownloadError):
        spider.download(url, dst, maximum_size=1024) # will not download
    assert os.path.exists(dst) is False
    
    spider.download(url, dst) # will not download
    assert os.path.exists(dst) is True
    
    
if __name__ == "__main__":
    import os
    pytest.main([os.path.basename(__file__), "--tb=native", "-s", ])