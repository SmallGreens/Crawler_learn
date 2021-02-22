"""
除了使用 xpath 外，python 还可以使用一个 另一个简洁方便的 html 或者 xml 解析工具，称为 beautiful soup。

beautiful soup 的使用依赖于其他的解析器， 它支持 python 标准库中 的 html 解析器，以及 lxml 解析器等。 一般的，基于效率、功能；推荐基于 lxml
解析器 使用 beautiful soup。
"""
from bs4 import BeautifulSoup

if __name__ == '__main__':
    '''
    安装：
        - beautiful soup 官方文档： https://www.crummy.com/software/BeautifulSoup/bs4/doc/
        - pip install beautifulsoup4
    
    使用：
        - step1：调用 BeautifulSoup 的构造函数 获取 BeautifulSoup 对象。
        - 通过 `.tag名称` 的方式获取 Tag 对象。
        - 通过调用 Tag 对象的属性获取相关的 Tag 信息：
            - string 属性，获取 tag 中的文本信息：
            - name 属性，获取 tag 的名字；
            - attrs 获取所有的属性 键值对；
            - attrs['属性名'] 获取 tag 对应的属性值, 更简单的，直接省略 attrs， [‘属性名’] 来获取节点对应的属性值
            
    选择时可以根据结点之间的关系进行结点的定位：
        - 嵌套选择：结点之间的 父子关系，来逐层选择
        - 关联选择：先选取一个结点，然后根据：
            - 父子关系 children, descendants, parent, parents 关键字；
            - 兄弟关系，next_sibling, previous_sibling, next_siblings, previous_siblings
            
    方法选择器：-- 通过在函数参数中传入待选取结点的 name，attrs，text 等来选取对应结点
        - find_all() -- 返回所有匹配的结果
        - find() -- 只返回第一个匹配的结果
        - CSS 选择器， beautifulSoup 支持 CSS 选择器，方法是使用 select() 函数，将 css 选择器传入该函数即可
            
    '''
    html_file = open('test.html', 'r', encoding='utf-8')  # 从本地读取 html 文件的方式
    soup = BeautifulSoup(html_file, 'lxml')  # 使用 lxml 解析器 构建一个 beautifulsoup 对象
    print(soup.prettify())   # beautifulSoup 对编码似乎处理的更好

    print(soup.title)  # 输出：<title>Test html file.</title>
    print(type(soup.title))  # 类型是： <class 'bs4.element.Tag'>
    print(soup.title.string)  # 输出： Test html file.  直接通过 .string 来获取 title 结点中的 文本信息

    print(soup.li)   # 只能获取 第一个 li， 后面的 li 结点会被忽略
    print(soup.li.attrs)  # {'class': ['cur'], 'data-id': ''} -- 获取所有的属性值，以 dict 的形式返回

    print(soup.li['class'])   # ['cur']

    for i, child in enumerate(soup.ul.children):  # children 所有 直接子节点。 descendants 所有子孙结点
        print(i, child)

    print(soup.find_all(attrs={'data-tag-id':'77953'}))  # 返回具有该属性的 Tag 对象
    print(soup.find_all(class_='title'))  # 由于 class 是 python 的关键字，查询 class 属性时，需要在最后添加一个下划线

    html_file.close()

    '''
    此外，如果熟悉 css 选择器，可以使用 pyquery 库对网页进行解析。
    '''
