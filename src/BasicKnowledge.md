# 基础知识

**HTTP**: hyper text transfer protocol- 超文本传输协议

**HTTPS**: hyper text transfer protocol over secure socket layer, 增强了安全性的 http，具体
是在 HTTP 下加入了 SSL 层。

## 1. 网页请求过程

请求，request，由客户端（通常是浏览器）发出，可以分为四部分内容：请求方法（request method）；
请求的网址（request URL）；请求头（request headers）； 请求体（request body）。

响应，response，主要分为三个部分：响应状态码（response status code）、响应头（response headers）
、 响应体（response body-- html 正文 or 其他资源文件）。

## 2. 网页基础

1. 构成：HTML, CSS, JavaScript


2. DOM - document object model，文档对象模型。HTML DOM 将 HTML 文档视作树结构，常被称为结点树。


3. 选择器：
    1. `#idName`, `.className`, `tagName` -- 最常见的三种选择方法。
    2. 嵌套选择。
    3. xpath
    
## 3. 爬虫基本原理

网络爬虫主要是进行自动化的网络信息提取，例如 html 网页，json 字符串，网页中的图片等。

现在网页前端越来越多的采用 Ajax、前端模块化工具来 构建 html 页面，我们得到的 html 可能整个的都是 JavaScript 
渲染出来的。这时候，我们就不能仅仅通过 urllib、requests 等库获取 html，还需要分析其后台的 Ajax 接口，或者
使用 Selenium、Splash 等库来模拟 JavaScript 的渲染。

## 4. 会话和 cookies

由于 http 协议的 无状态特性，客户端的每次请求对于 服务器来说都是独立的。

为了实现对 http 连接状态的保持，我们通过 会话和 cookies 来实现。会话是对于服务器端来说，设置的保存用户会话信息的
一段连接时间。而会话的保持，通常是通过 cookies 来实现，就是服务器下发特定的 cookies 给客户端，客户端在后续的 
请求连接中会携带相关 cookies，从而服务器能够自动的识别该客户，保持一个有效的会话。

根据会话持续的时间，可以分为 会话 cookie 和 持久 cookie，所谓 会话 cookie 一般是将 cookie 放置在 浏览器缓存中，
当浏览器关闭后，相关 cookie 会自动删除。而 持久 cookie 则保存在文件系统中，不会随浏览器的关闭而自动清理，
从而这种 cookie 的持续时间更久，具体过期时间由服务器端通过设定 max age/expires 字段决定。 

Remark: 

1. 可以认为 expires 为 session 的 cookies 存放在了浏览器缓存中，会随着浏览器关闭自动清理， 
而 expires 为具体时间的 cookies 则不会随着浏览器关闭而自动清理。
   
2. chrome 中查看 cookies： 'application -> storage -> Cookies' 

## 5. 代理

网站可能会采取限制单个 ip 单位时间内的访问次数的方法来反制爬虫。这时候，如果要保证爬取速度，就需要通过使用 
代理 的方式。

### 代理的基本原理

代理服务器 proxy server，实际上就是在本地客户机和远程服务器之间添加了一个中转。由于服务器只能看到向其发送请求的 
代理服务器，本地客户机能够被隐藏。

代理按照协议分类：FTP代理服务器，HTTP代理服务器，SSL/TLS代理服务器，SOCKS代理等。







