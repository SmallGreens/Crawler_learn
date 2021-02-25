"""
使用 模拟浏览器的方式爬取网页，这里介绍 selenium 的方案。 document: https://www.selenium.dev/documentation/en/
step1: 安装： pip install selenium
此外，还需要安装 chromedriver 或者 geckodriver（firefox） (或者直接安装无界面浏览器 PhantomJS)
这里使用 firefox 浏览器，deckodriver 下载地址： https://github.com/mozilla/geckodriver/releases/tag/v0.29.0
将下载好的 geckodriver.exe 直接放置到了 venv 的 script 目录下。

此外，selenium 还支持 android 手机端浏览器。

除了 selenium 外，还可以使用 splash 来进行动态渲染页面的爬取。splash 是 一个 JavaScript 渲染服务，是一个带有 http api 的轻量级浏览器，因此，
他可以相对独立的（selenium 需要安装 geckodriver 等浏览器驱动）进行 动态渲染页面的抓取。
link: https://splash.readthedocs.io/en/stable/
"""


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def test():
    """
    例子： 使用 selenium 完成访问百度，搜索 python 并返回搜索结果
    :return:
    """
    # step1: 初始化 - 返回一个浏览器 browser 对象
    browser = webdriver.Firefox()
    try:
        # step2: 访问页面
        browser.get('https://www.baidu.com')

        # 可以获取网页中的结点：
        '''
        find_element_by_id() -- 根据结点 id 查找
        find_element_by_css_selector -- 使用 css 选择器查找
        find_element_by_xpath() -- 使用 xpath 查找结点
        '''
        input = browser.find_element_by_id('kw')
        input.send_keys('python')
        input.send_keys(Keys.ENTER)
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'content_left')))
        print(browser.current_url)
        print(browser.get_cookies())
        print(browser.page_source)  # 返回页面源码
    finally:
        browser.close()


if __name__ == '__main__':
    '''
    步骤总结：
        1. 获取浏览器对象， selenium.webdriver.Firefox() or 其他浏览器 `browser = webdriver.Firefox()`
        2. 使用 1 中获取的浏览器对象访问页面，`browser.get('https://www.baidu.com')`
        3. 获取相关资源
            1. browser.page_source -- 获取网页源码
            2. browser.get_cookies() -- 获取 cookies
            。。。
        4. 查找结点
            1. 查找单个结点：find_element_xx
                通过 id，xpath，css选择器 查找结点。 find_element_by_id()， find_element_by_css_selector() 等方法。
            2. 一次查找多个结点  find_elements_x
        5. 结点交互
            1. 输入文字：send_keys(), 清空文字 clear(), 
            2. 点击按钮：click()
        6. 执行 JavaScript
            对于某些 selenium 没有提供的操作，可以通过 js 代码来实现。
            e.g. `browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')` # 将网页拉到最底
        7. 获取节点信息
            可以直接使用 selenium 来解析网页（代替 beautifulSoup，pyquery等）-- 略
        8. 切换 Frame
            selenium 打开默认位于页面的父级 frame 中，但对于有子 frame（iframe）的页面来说，需要进行切换。
        9. 延时等待
            get 方法执行完毕立即获取 page_source 可能并不是完整的浏览器加载的完成后的页面（部分ajax 请求可能还没有完成），因此需要等待一会儿。
            browser.implicitly_wait(10)  # 等待10s
            或者使用上述访问百度例子 中的代码。
            其实也可以直接 time.sleep() 
        10. 前进和后退
            。。。
    '''
    test()
