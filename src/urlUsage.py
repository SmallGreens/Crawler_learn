import http
import urllib.request
import urllib.parse
from urllib.error import URLError
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
import http.cookiejar
from urllib.parse import urlparse, urlunparse, urlencode
from urllib.robotparser import RobotFileParser

if __name__ == '__main__':
    '''
    urllib 的使用
        request module:
            urlopen 方法，直接打开一个 url 返回一个 HTTPResponse 对象。然后可以使用相关方法获取该 response 各部分的信息。
            Request 类：  urllib.request.Request('url') # 创建一个 request 对象
            更高级的处理例如：cookies，登录验证，代理设置，可以通过一个个的 handler 来处理。在 request module 中，
                BaseHandler 是所有 Handler 的父类，提供一些公用方法；
                HTTPCookieProcessor: 用于处理 cookie 的handler
                ProxyHandler, 用于处理代理相关的 handler 
                HTTPBasicAuthHandler: 用于管理认证。
            OpenerDirector 类，用于配合 handler 生成更高级的 opener -- urlopen 是 request module 封装好的最基本的opener
                但需要具有额外功能的 opener，就需要使用 OpenDirector 自定义 opener 
                然后，调用 opener 对象的 open() 方法，来处理 request 对象（or 简单的 url） -- ref 下方例子代码
        
        Error 的处理
            在 urllib 库中，error module 用于处理由 request module 产生的异常
            URLError, 继承自 OSError，是 error module 中异常的 base class，如果不清楚具体异常，request module 中所有异常都可以用它处理
            HTTPError, 专门用于处理 http 请求错误。
            
        解析链接 - parse module
            parse module 中定义了处理 URL 的相关函数， 支持多种协议的url，e.g. http, https, ftp, file, imap .....
            具体参考下方的代码演示
        
        robotparser
            robots 协议 全称为 robots exclusion protocol， 用来告诉网络爬虫和搜索引擎那些页面可以抓取，哪些不可以抓取。
            通常，该协议内容会以 robots.txt 的形式放置在网站的根目录下。搜索引擎会首先寻找该文件，然后根据该文件中规定的范围进行爬去
                如果搜索引擎无法找到 robots.txt 文件， 则默认的会对所有可以直接访问的页面进行爬取
            urllib 中的 robotparser 模块可以用于解析 robots.txt 文件，主要通过类 RobotFileParser 来实现
            
    '''

    response = urllib.request.urlopen('https://www.python.org')
    print(type(response))  # <class 'http.client.HTTPResponse'>
    # print(dir(http.client.HTTPResponse))   # 查看该对象的方法，属性
    # print(response.read().decode('utf-8'))  # read() 方法，查看 html 内容
    print(response.status)  # response 状态码： 200
    print(response.getheaders())
    print(response.getheader('server'))  # 返回： nginx

    print('*' * 40)
    # 用于测试 https 请求、响应的工具
    # 添加 urlopen() 添加 data 参数，变为 post 请求。该 data 需要首先转码为 bytes （字节流）类型
    data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf-8')
    response = urllib.request.urlopen('http://httpbin.org/post', data=data)
    print(response.read().decode('utf-8'))  # 如果不添加 .decode('utf-8')，‘\n’ 等内容无法正确显示。

    # Request 类的使用
    url = 'http://httpbin.org/post'
    headers = {   # 可以自定义头，来模拟真实的浏览器访问，默认的 'User-Agent' 是 Python-urllib/3.8
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0',
        'host' : 'httpbin.org'
    }
    request = urllib.request.Request(url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(request)
    print(response.read().decode('utf-8'))

    '''
    更复杂的请求：演示 handler 和 OpenerDirector 的使用
    '''

    username = 'username'
    pwd = 'password'
    url = 'http://localhost:5000/'

    p = HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, username, pwd)
    auth_handler = HTTPBasicAuthHandler(p)  # 生成一个 handler 对象
    opener = build_opener(auth_handler)     # 配合该 OpenerDirector 对象生成一个

    '''
    try:
        res = opener.open(url)
        html = res.read().decode('utf-8')
        print(html)
    except URLError as e:
        print(e.reason)
    '''

    # cookies 相关
    cookie = http.cookiejar.CookieJar()   # collection of http cookies
    handler = urllib.request.HTTPCookieProcessor(cookie)   # 构建 handler
    opener = build_opener(handler)  # 使用该 handler 生成 opener
    response = opener.open('http://www.baidu.com')
    for item in cookie:             # cookies 里面是一个个键值对
        print(item.name + ': ' + item.value)
    '''
    输出：
    BAIDUID: A77E65EA9A024E148FE4D6EC80A2BE4D:FG=1
    BIDUPSID: A77E65EA9A024E14A9A7235FF1637A87
    H_PS_PSSID: 33423_33403_33272_26350_33568
    PSTM: 1613733292
    BDSVRTM: 0
    BD_HOME: 1
    '''
    # 将 cookie 保存到文件
    filename = 'cookies.txt'
    cookie1 = http.cookiejar.MozillaCookieJar(filename)  # MozillaCookieJar 是 CookieJar 的子类，cookies与文件相关的操作用它
    # 它将 cookies 保存成 mozilla 浏览器的 cookie 格式。
    # 后序可以再使用它 从文件中读取 cookies
    handler1 = urllib.request.HTTPCookieProcessor(cookie1)
    opener1 = build_opener(handler1)
    response1 = opener1.open('http://www.toutiao.com')
    cookie1.save(ignore_discard=True, ignore_expires=True)

    '''
    解析链接模块的使用演示
    '''

    result = urlparse('https://www.terasic.com.tw/page'
                      '/archive.pl;test?Language=English&PartNo=4#f')
    print(type(result), '\n', result)
    '''
    输出：
    <class 'urllib.parse.ParseResult'> 
    ParseResult(scheme='https', netloc='www.terasic.com.tw', path='/page/archive.pl', params='test', query='Language=English&PartNo=4', fragment='f')
    
    标准 url 格式为： scheme://netloc/path;param?query@fragment
    scheme: 为协议
    netloc: 为域名
    path: 访问路径
    param: 分号后为 param
    query: 问号后为 query内容
    fragment：锚点，一般为 # 后面的值
    '''
    # urlunparse, 将数据组成 url
    data = ['http', 'www.baidu.com', 'index.html', 'user', 'a=6','comment']
    print(urlunparse(data))  # 将数据组合成 url

    # urlencode 将 dict 等插入到 url 中
    # https://www.baidu.com/s?tn=news&word=xiaomi+car
    query = {'tn': 'news', 'word': 'xiaomi car'}
    base_url = 'http://www.baidu.com?'
    url = base_url + urlencode(query)
    print(url)

    '''
    robot 协议：
        例子：https://ieeexplore.ieee.org/robots.txt
        User-agent: *
        Disallow: /rest
        Disallow: /ielx*
        User-agent: Twitterbot
        User-agent: facebookexternalhit/1.1
        User-agent: facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)
        
        Allow: /*.jpg$
        Allow: /*.jpeg$
        Allow: /*.gif$
        Allow: /*.png$
        
        解释： User-agent: 描述了搜索爬虫的名称， 如果为 *  -- 表示对任何爬虫有效
        Disallow: 为不允许抓取的目录
        allow: 通常和 disallow 一起使用，表名在上述 disallow 的目录中，排除相关的内容
        
    '''

    # urllib 中使用 robotparser 模块的 RobotFileParser 类来 解析 robots.txt 以及判断一个网址是否允许爬取
    rp = RobotFileParser()
    # rp.set_url('http://www.jianshu.com/robots.txt')
    # robots = urllib.request.urlopen('https://www.jianshu.com/robots.txt') -- 简书的 这个获取时报:  HTTP Error 403
    rp.set_url('https://www.toutiao.com/robots.txt')
    rp.read()
    print(rp.can_fetch('*', 'https://www.toutiao.com/about/'))  # 不知道为何总是 返回 False，但似乎这个是在 allow 里面的
    print(rp.can_fetch('*', 'https://www.toutiao.com/a6930872876555829768/'))


