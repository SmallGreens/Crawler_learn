
# Scrapy framework

Scrapy 是一个爬虫框架，它功能强大，相关组件多， 可配置可扩展性好，几乎可以应对所有反爬网站，是目前 python 中使用最广泛的爬虫框架。

Official site: <https://scrapy.org/>. 
## Scrapy 介绍

scrapy 是一个 基于 Twisted 的异步处理框架， 它主要由以下几个部分组成：

- Engine：引擎，处理整个系统的数据流，触发事务，是整个 scrapy 的核心；
- Item: 项目，定义爬取结果的数据结构；
- scheduler：调度器，接收引擎发送过来的请求并将其加入队列中。
- downloader：下载器， 下载网页内容，并将网页内容返回给 spider。
- spider：定义对爬取网页的解析规则；
- item pipeline： 负责 对 spider 解析出的数据进行进一步清晰，验证 和数据的存储；
- downloader middleware: 引擎和下载器之间， 处理引擎与下载器之间的请求及响应；
- spider middleware: 位于 引擎和spider 之间，主要处理 spider 输入的响应和输出的结果及新的请求。

Scrapy 的 **处理流程** 是这样的：

- 初始准备：engine 首先获得一个 url，处理该网站的  spider 获取该 url 中需要爬取的 连接link；
    -- 例如要爬取网页中的图片，首先传入原网页，spider 从中解析出 图片地址；
- step1： scheduler 将需要爬取的 url 放入队列中；
- step2: engine 从 scheduler 获得需要爬取的 url；
- step3: engine  将 step2 中获得的 url 通过 downloader middleware 转发给 downloader 进行下载 ；
- step4: downloader 下载完毕页面， 将该页面的内容返回给 engine，再由 engine 将它 经由 spider middleware 交给 spider 进行解析；
- step5: spider 对网页进行解析，返回解析出来的 item 以及 新的 request 请求url 一起交给 engine，
    -- engine 将 item 交给 item pipeline 进行处理， 新的 request 交给 scheduler 推入队列。

通过上述的介绍，我们总结如下：

- scrapy 为了能够处理更加大型的爬虫工程，将爬虫工作根据具体的 工作内容进行了拆分：
    - schedule：相当于一个消息队列，放置需要进行请求的内容；
    - downloader： 负责除了 request、response，获取原始的网页内容；
    - spider 负责进行解析；
    - item pipeline： 负责数据的清洗存储。

# scrapy 项目的结构

通常，一个 scrapy 项目的结构如下：

    - scrapy.cfg (scrapy 的配置文件)
    - project/
        - __init__.py
        - items.py (定义 item 数据结构)
        - pipelines.py  (定义 item pipeline 的实现)
        - settings.py   (定义项目的全局设置)
        - middlewares.py  (定义 spider middleware 和 downloader middleware 的实现)
        - spiders/  (放置spider 的实现)
            __init__.py
            spider1.py
            spider2.py