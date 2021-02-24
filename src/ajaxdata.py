"""
参考 ajaxdata.md 文档。

以 微博为例子： https://m.weibo.cn/u/7097382157

分析它的 ajax 请求，请求地址为： Request URL: https://m.weibo.cn/api/container/getIndex?type=uid&value=7097382157&containerid=1076037097382157

参数部分： type=uid&value=7097382157&containerid=1076037097382157。 使用 uid 定位该用户，container id 定位具体内容

查看返回的 response， 发现页面中的 内容信息都放置在了 json 串的 data -> card 元素中。 默认的一次刷新出 9 个 card。
cards: [{card_type: 9, itemid: "1076037097382157_-_4574740931416831"
每个 card 中， mblog 字段是具体微博信息，包括该微博内容的相关属性，以及资源文件，包括文本信息（text字段）。
"""

from urllib.parse import urlencode
import requests
from pyquery import PyQuery as pq

base_url = 'https://m.weibo.cn/api/container/getIndex?'

headers = {
    'Host': 'm.weibo.cn',
    'Referer': 'https://m.weibo.cn/u/7097382157',
    'User-Agent': 'Mozilla/5.0 (Windows NT 7.0; Win64; x64) AppleWebKit/557.31 (KHTML, like Gecko) Chrome/81.0.44324.342',
    'X-Requested-With': 'XMLHttpRequest'
}


def get_page():
    """获取页面的方法"""
    params={
        'type': 'uid',
        'value': '7097382157',
        'containerid': '1076037097382157',
    }
    url = base_url + urlencode(params)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
    except requests.ConnectionError as e:
        print('Error', e.args)


def parse_page(json):
    """解析数据"""
    if json:
        items = json.get('data').get('cards')
        for item in items:
            item = item.get('mblog')
            weibo = {'id': item.get('id'),
                     'text': pq(item.get('text')).text(),  # 为啥用 beautifulsoup(item.get('text'), 'lxml').string 就不行？
                     'comments': item.get('comments_count')}  # dict
            yield weibo


if __name__ == '__main__':
    json = get_page()
    res = parse_page(json)
    for i in res:
        print(i)
