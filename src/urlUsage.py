import http
import urllib.request
import urllib.parse
from urllib.error import URLError
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener

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

    # 演示 handler 和 OpenerDirector 的使用
    username = 'username'
    pwd = 'password'
    url = 'http://localhost:5000/'

    p = HTTPPasswordMgrWithDefaultRealm()
    p.add_password(None, url, username, pwd)
    auth_handler = HTTPBasicAuthHandler(p)  # 生成一个 handler 对象
    opener = build_opener(auth_handler)     # 配合该 OpenerDirector 对象生成一个

    try:
        res = opener.open(url)
        html = res.read().decode('utf-8')
        print(html)
    except URLError as e:
        print(e.reason)




