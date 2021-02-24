# 简述

在浏览器中，我们查看 request 得到的 response 可能与实际在浏览器看到的网页源码并不相同。这是因为 request 获得的仅仅是原始 html 页面，而浏览器实际
呈现的，是经过 JavaScript 处理过的页面。

通过 JavaScript 处理的方案有很多， 一种非常常用的办法，就是通过 ajax 进行加载。

ajax 的全称是 asynchronous JavaScript and xml. 是一种异步的请求，原始页面加载完毕后，再向服务器 发送 ajax 请求，
获得接口数据，从而完成页面的动态渲染。

最典型的例子包括网页中的“加载更多” 功能，通常是使用 ajax 来实现的，并不重新请求网页，而是在当前网页中 通过 JavaScript 进行动态的渲染。

总的来说，ajax 的操作可以分下面3个步骤：

1. 发送请求；
2. 解析内容；
3. 完成渲染。 

# 分析 AJAX

了解了 ajax 的基本原理之后， 爬取 ajax 请求的内容需要我们对网站的 ajax 请求进行分析。

在 浏览器中进入开发者选项卡，进入 network 分析页面，ajax 请求的类型为 xhr，筛选该类型的请求，就可以查看到本页面中
的所有 ajax 请求。 

查看 ajax 请求的 request headers, 其中 `X-Requested-With: XMLHttpRequest`, 标明了 该请求为 ajax 请求。

点击 preview, 可以查看 该 ajax 请求的响应内容-通常为 json 格式，浏览器会帮助我们将response 解析为方便查看的形式；
点击 response 选项卡，可以查看到 原始的 请求response 文本。

通过分析 ajax 请求的地址，以及返回的 json 串内容，我们从中提前需要的信息。
