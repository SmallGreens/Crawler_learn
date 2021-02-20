"""
link: https://maoyan.com/board/4
分析: 第二页为： link: https://maoyan.com/board/4?offset=10
"""
import json
import re
import time

import requests
from requests.cookies import RequestsCookieJar


def get_one_page(url):
    # 同一个 header 请求次数太多就被要求验证。把 header 稍微改一下就行了。
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Chrome/70.5'}
    ''' may use cookies. 
    cookies = 'xxx'
    jar = RequestsCookieJar()
    for cookie in cookies.split(';'):
        li = cookie.split('=', 1)
        jar.set(li[0].strip(), li[1].strip())
    response = requests.get(url, headers=headers, cookies=jar)
    '''
    response = requests.get(url, headers=headers)
    print(response.status_code)
    if response.status_code == 200:
        return response.text
    return None


def parse_one_page(html):
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?title="(.*?)".*?data-src="(.*?)"'
                         '.*?<p class="star">(.*?)</p>.*?"releasetime">(.*?)</p>.*?</dd>', re.S)
    items = re.findall(pattern, html)
    for item in items:
        yield {
            'index': item[0],
            'title': item[1],
            'image': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:]
        }


def write_to_file(content):
    """将字典写入到文本中"""
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')  # 为了中文显示正确， 设置 ensure_ascii=False


def main(offset):
    url = 'https://maoyan.com/board/4?offset='+str(offset)
    html = get_one_page(url)
    print(html)
    for item in parse_one_page(html):
        print(item)
        write_to_file(item)


if __name__ == '__main__':
    for i in range(10):
        main(offset=i * 10)
        time.sleep(10)  # 将 sleep 时长度增加了，仍然不行。爬取 4 页后就停止了。

    '''
    note: 分析源码时，查看 network 中返回的原始源码，而不要看 elements 中显示的源码。因为 elements 中的代码可能是经过 JavaScript 操作过后的内容
    
    step1: 分析 url，编写 get_one_page() 函数获取网页内容
    step2: 分析网页内容，解析有效信息 -- 这里 使用最基础的正则表达式实现
        - 此外，将返回的 list 信息处理为 dict 格式，进而方便后序存储为 json 串
    step3: 文件存储，格式化为 json 串并存储到文件中
    '''

    '''
    step2: 分析网页内容-- 细节
    选取复制一部电影的 html 元素进行分析，编写正则表达式。 将 html 放置到 vscode 中，`shift + alt + F` 将html 代码自动格式化。
    <dd>
        <i class="board-index board-index-13">13</i>
        <a href="/films/1633" title="阿甘正传" class="image-link" data-act="boarditem-click" data-val="{movieId:1633}">
            <img src="//s3plus.meituan.net/v1/mss_e2821d7f0cfe4ac1bf9202ecf9590e67/cdn-prod/file:5788b470/image/loading_2.e3d934bf.png"
                alt="" class="poster-default" />
            <img data-src="https://p0.meituan.net/movie/b41795c4a88479137e40ebdc3d7dc040238291.jpg@160w_220h_1e_1c"
                alt="阿甘正传" class="board-img" />
        </a>
        <div class="board-item-main">
            <div class="board-item-content">
                <div class="movie-item-info">
                    <p class="name"><a href="/films/1633" title="阿甘正传" data-act="boarditem-click"
                            data-val="{movieId:1633}">阿甘正传</a></p>
                    <p class="star">
                        主演：汤姆·汉克斯,罗宾·怀特,加里·西尼斯
                    </p>
                    <p class="releasetime">上映时间：1994-07-06(美国)</p>
                </div>
                <div class="movie-item-number score-num">
                    <p class="score"><i class="integer">9.</i><i class="fraction">4</i></p>
                </div>
            </div>
        </div>
    </dd>
    
    reg_ex: 排名 -  电影名 -  图片 -  主演 - 上映时间
    <dd>.*?board-index.*?>(.*?)</i>.*?title="(.*?)".*?data-src="(.*?)".*?<p class="star">(.*?)</p>.*?"releasetime">(.*?)</p>.*?</dd>
    data src ＝”（．的）”．盯name . 盯a.*?>(.*?)</a ＞.的star . 的〉（ ． 的）＜／ p>.*?releaset
ime.*?>(.*?)</p> . *?integer. 叼＞（.＊？）＜／ i> . *?fraction . *?>(.*?)</i>.*?</dd>
    '''
