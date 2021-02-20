import re
from urllib.parse import urlparse
import requests
from requests.cookies import RequestsCookieJar


if __name__ == '__main__':
    '''
    学习 requests 库的使用。
    
    requests 库是 python 中一个更为强大的、简洁的 处理高级 网络相关操作的库。 
    
    step1：安装 requests 库
        默认 python 不自带 requests 库，需要进行安装，github: https://github.com/psf/requests
        安装： 在 ide 的 terminal 中，venv 环境下执行： pip install requests 
        安装信息：pip 版本：21.0.1， certifi-2020.12.5 chardet-4.0.0 idna-2.10 requests-2.25.1 urllib3-1.26.3
        
    重要方法简介：
    '''

    '''1-- 更加简洁的实现 get，post，以及获取 response 中的相关参数'''
    r = requests.get('https://www.baidu.com/')
    print(r.status_code)  # 200
    print(type(r))   # <class 'requests.models.Response'>
    # print(r.text)
    # -- 这里的 cookies 不同是因为 没有添加 headers 的缘故
    print(r.cookies)  # <RequestsCookieJar[<Cookie BDORZ=27315 for .baidu.com/>]>

    r = requests.post('http://httpbin.org/post')  # post 请求也可以一句话完成
    print(r.text)

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Firefox/85.0'}
    r = requests.get('http://www.jianshu.com', headers=headers)
    print(r.status_code)   # 使用 status_code 判断是否 请求成功，如果不加 headers， 返回 403， 加了之后，200

    '''2-- 可以使用 requests 更加简洁地构建 复杂的 请求 url'''
    print(urlparse('http://httpbin.org/get?name=germey&age=22'))
    data = {
        'name': 'feifei',
        'age': 22
    }
    r1 = requests.get("http://httpbin.org/get", params=data)  # 这里用 params 参数！！ 而不是 query=data
    print(r1.text)  # 构建出的 url为："url": "http://httpbin.org/get?name=feifei&age=22"
    a = r1.json()  # 如果返回的是 json 格式，可以直接使用 requests 的 json() 函数将其转为 dict
    print(type(a), '\n', a)  # <class 'dict'>

    '''演示1- 抓取网页'''
    r = requests.get('https://www.zhihu.com/explore', headers=headers)  # 如果不添加 header 信息： 403 Forbidden
    # 通过分析 网页，撰写正则表达式，来提取相关问题的 title
    pattern = re.compile('ExploreRoundtableCard-questionTitle.*?>(.*?)</a>', re.S)
    titles = re.findall(pattern, r.text)   # 返回一个 list
    print(titles)

    '''演示2- 抓取图片 -- 类似的，音频视频文件也可以这么获取'''
    # 图片是 binary 的文件
    r = requests.get('https://images.nowcoder.com/images/xmas/images/20191224/4107856_1577154253860_5D1BFB3D4CCCFAD1978E23D1526A7ED3')
    # print(r.content)  # 'b'\x89PNG\r\n\x1a\n\x00\x00\x00\rI .... ' 是一堆二进制数
    with open('example.png', 'wb') as f:
        f.write(r.content)

    '''高级用法1：上传文件'''
    files = {'file': open('example.png', 'rb')}
    r = requests.post('http://httpbin.org/post', files=files)
    # print(r.text)   # 返回的 json 串中，会有： "files": { "file": "data:application/octet-stream;bas...}

    '''高级用法2： 处理 cookies'''
    r = requests.get('http://www.baidu.com', headers=headers)
    for key, value in r.cookies.items():
        print(key, '=', value)   # 不添加 headers --》 BDORZ : 27315， 添加 headers 和 urllib 中返回的 cookies 相同
    # 将 cookies 设置到 request 中
    cookies = 'BIDUPSID=AF495EDF0B65A705CAD67052D5817A22; ' \
              'PSTM=1613802929; BAIDUID=AF495EDF0B65A705B143C36E05F5057E:FG=1; ' \
              'BD_HOME=1; H_PS_PSSID=33425_33355_33258_33344_33463_33584_26350_22157; ' \
              'BD_UPN=12314753; BA_HECTOR=218ka185ak25ak2h5f1g31bdh0r'      # baidu 的 cookies
    jar = RequestsCookieJar()  # 将 cookies 放置到 requests.cookies.RequestCookieJar 类的实例中
    for cookie in cookies.split(';'):
        li = cookie.split('=', 1)
        jar.set(li[0].strip(), li[1].strip())
    r = requests.get('http://www.baidu.com', headers=headers, cookies=jar)
    print(r.status_code)

    '''高级用法3：会话维持 -- 模拟浏览器中的一次会话，请求中保持 cookies 等内容'''
    s = requests.Session()   # 新建一个 Session 类的实例
    s.get('http://httpbin.org/cookies/set/number/123456')  # 测试网站：设置一个 cookie： number: 123456
    r = s.get('http://www.httpbin.org/cookies')     # 使用 session 进行操作可以保持请求的 cookie 相同
    print(r.text)

    '''
    其他高级功能：
        - SSL 证书验证：在 requests.get() 中设置 `verify=false` 或者指定证书：`cert=('path/server.crt', 'path/key')`-- ssl 认证包括 秘钥和证书
        - 代理设置：在 requests.get() 中设置 proxies 参数
        - 超时设置，在 get() 函数中设置 timeout 参数
        - 身份认证：在 get() 函数中设置 auth=HTTPBasicAuth(xx). requests 还支持其他认证，例如 OAuth，但需要安装 oauth 包： pip install requests_oauthlib 
    '''
