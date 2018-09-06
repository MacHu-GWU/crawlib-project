#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import shutil
from pathlib_mate import Path
from crawlib.downloader.selenium_downloader import ChromeDownloader

chromedriver_executable_path = Path(Path.home(), "chromedriver")

if chromedriver_executable_path.exists():
    cache_dir = Path(__file__).change(new_basename=".cache").abspath
    dl_dst = Path(__file__).change(new_basename="python.org.html").abspath

    def reset():
        try:
            shutil.rmtree(cache_dir)
        except:
            pass

        try:
            os.remove(dl_dst)
        except:
            pass

    class Test(object):
        def test(self):
            with ChromeDownloader(
                    chromedriver_executable_path=chromedriver_executable_path.abspath,
                    cache_dir=cache_dir,
                    read_cache_first=True,
                    alert_when_cache_missing=True,
                    always_update_cache=True,
                    cache_expire=24 * 3600,
            ) as dl:
                url = "https://selenium-python.readthedocs.io/"
                html = dl.get_html(url)
                assert "Selenium" in html
                assert "Python" in html

                with pytest.raises(NotImplementedError):
                    dl.download(url=url, dst="selenium-python.html")
else:
    msg = ("INFO: in order to test `ChromeDownloader`, "
           "place the chromedriver executable file under ${HOME} directory.")
    print(msg)

if __name__ == "__main__":
    import os

    basename = os.path.basename(__file__)
    pytest.main([basename, "-s", "--tb=native"])
