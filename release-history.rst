Release and Version History
===========================


0.0.26 (TODO)
~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.25 (2018-09-06)
~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``crawlib.downloader.selenium_downloader`` module
- move disk cache relative code into ``crawlib.cache.CacheBackedDownloader``
- add a job executor function for mongodb backed, one-to-one, one-to-many architecture.

**Minor Improvements**

- add more methods for ``crawlib.logger.SpiderLogger``

**Miscellaneous**

- remove ``crawlib.spider`` sub package.


0.0.24 (2018-09-05)
~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- now allows ``OneToManyItem._settings_N_CHILD_1_KEY_optional`` to be None. Then ``{n_child}`` field will not be updated.
- improve code coverage.


0.0.23 (2018-08-21)
~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- add ``\n`` at the head of each line of ``sys.stdout.write(line)``.


0.0.22 (2018-08-19)
~~~~~~~~~~~~~~~~~~~
**Minor Improvements**

- Add ``RequestDownload.alert_when_cache_missing`` option, allow it print alert when cache is missing. Of course you need to turn on ``RequestDownload.read_cache_first = True``.

**Bugfixes**

- Fix a fetal type bug in creating proxy for session in ``RequestDownload.__init__`.


0.0.21 (2018-08-16)
~~~~~~~~~~~~~~~~~~~
**Bugfixes**

- Fix a fetal bug in creating proxy for session in ``RequestsDownloader.__init__``.


0.0.20 (2018-08-15)
~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add ``SpiderLogger`` class.

**Minor Improvements**

- add some ``set_status`` methods for ``ParseResult``.
- improve tet coverage.

**Bugfixes**

- it should call ``requests.Session`` instead of ``requests.session`` in ``RequestsDownloader``.


0.0.19 (2018-08-14)
~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- allow user to customize the cache behavior. ``RequestsDownloader.read_cache_first``, ``RequestsDownloader.always_update_cache`` these two option variable can be used to adjust cache behavior.


0.0.18 (2018-08-14)
~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- add a downloader middleware, integrate with auto rotate headers, disk cache, tor network support.


0.0.17 (Milestone)
~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- breaks lots of backward compatibility.
- rewrite ``crawlib.data_class.ParseResult`` and ``crawlib.data_class.ExtendedItem``.
- add a ``crawlib.pipeline`` module, add integration with mongodb and relational database.

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.0.1 (2016-08-29)
~~~~~~~~~~~~~~~~~~
- First release