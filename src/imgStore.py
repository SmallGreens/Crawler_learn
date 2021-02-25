"""
爬取并保存图片
link: https://www.toutiao.com/a6932274194793234956/

"""
import os

import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver


def get_html(url):
    browser = webdriver.Firefox()
    try:
        browser.get(url)
        html = browser.page_source
        browser.implicitly_wait(10)
        with open('toutiao.html', 'w', encoding='utf-8') as f:
            f.write(bs(html, 'lxml').prettify())
    finally:
        browser.close()


def save_img():
    # step1: 打开网页资源
    html_file = open('toutiao.html', 'r', encoding='utf-8')
    soup = bs(html_file, 'lxml')
    fig = soup.find_all(attrs={'class': 'syl-page-img'})  # 返回一个 list
    name = 0
    for i in fig:
        name += 1
        url = i.attrs['src']  # 获取 src 属性
        try:
            response = requests.get(url)
            file_name = 'Fig{0}.jpeg'.format(name)
            if not os.path.exists(file_name):
                with open(file_name, 'wb') as f:
                    f.write(response.content)
            else:
                print('already downloaded. ', file_name)
        except requests.ConnectionError:
            print('failed to save fig.')


if __name__ == '__main__':
    # get_html('https://www.toutiao.com/a6932274194793234956/')
    save_img()