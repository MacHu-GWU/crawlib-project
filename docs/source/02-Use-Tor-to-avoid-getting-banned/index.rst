Use Tor to avoid Getting Banned
==============================================================================

洋葱网络的原理是这样的:

洋葱网络的核心是一个叫Onion Routing的协议. 这个协议是, 只要你同意遵守这个协议, 并愿意将你的电脑放在网上作为洋葱路由的一个节点. 那么其他使用洋葱网络的人就可以随机的在网络中选择若干个节点作为中转站, 期间所有端对端都进行加密, 这样最终你访问的网站就无法知道真正的请求是从哪里来的. 而我们可以通过设置, 没几秒就刷新一下路由, 这样我们的爬虫就不可能被Ban了.

- 如果你想使用洋葱浏览器进行匿名上网, 那么你要到 https://www.torproject.org/download/download-easy.html.en 下载洋葱浏览器软件. 洋葱浏览器会自动连上洋葱网络, 当浏览器关闭时会自动断开. 只有通过洋葱浏览器浏览时才是通过洋葱网络进行的匿名访问. 开着洋葱浏览器而用chrome浏览网页是没有效果的.
- 如果你想要在机器上运行洋葱网络的服务, 然后通过本机的一个端口去和外网通信, (这通常应用于你想用编程来对洋葱网络进行访问的情况). 那么请参考这个教程 https://www.torproject.org/docs/tor-doc-osx.html.en , 使用包管理软件安装tor, 然后使用以下三个命令 ``启动``, ``重启``, ``关闭`` 对洋葱网络进行操作.

    - ``brew services start tor``
    - ``brew services restart tor``
    - ``brew services stop tor``

执行了 ``brew services start tor`` 并且成功之后, 你需要装 ``requests`` 和 ``pysocks`` 两个包. 由于默认洋葱路由的端口是9050, 所以下面的代码就可以通过洋葱路由来上网了.

.. code-block:: python

    import requests

    ses = requests.Session()
    ses.proxies = {
        "http": "socks5h://localhost:9050",
        "https": "socks5h://localhost:9050",
    }
    ses.get(url)
