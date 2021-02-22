"""
爬虫实际上可以分为两部分的工作，一部分是通过网络请求，获取资源, 例如网页资源或者 json 串。

第二部分的工作则是从获取的资源中提取有效的信息，例如之前的例子中，从网页中提取电影相关的信息， 之前的例子中使用了 正则表达式的方法进行提取，
更方便的，我们可以利用 网页 DOM 的结构，从网页中提取需要的信息。 最常用的有两种方式： CSS 选择器  和 XPATH .
"""
from lxml import etree

if __name__ == '__main__':
    '''
    本节介绍 xpath 的使用
        XPath 全称为 xml path language，即 xml 路径语言，用于在 xml 中查找信息。
        python 中可以通过安装 lxml 库 来使用 xpath 语言解析 html。 官网：https://lxml.de/
            - pip install lxml    
            
    在 python 中，使用 xpath 表达式之前，需要将网页内容转化为 支持 xpath 函数的 ElementTree 对象。使用 etree module 中的方法进行对象的创建。
    ElementTree 对象构建完成之后，就可以使用 xpath 中的语法对对象进行解析，提取 需要的结点中的内容
    表达式规则介绍：
        - '/': 直接子节点； '//' 子孙结点；
        - '..': 父节点    
        - [@href="xxxx"]：属性匹配。 @xx: 属性获取
        - 文本获取，获取节点中间的文本 text() 
        - 按顺序选择节点：节点[x], 获取第 x 个对应结点的内容， last() 对应结点的最后一个结点， position() < k， 前 k 个结点
        - 结点轴选取：//li[1]/ancestor::*, 获取第 1 个 li 结点的所有的祖先结点；//li[1]/attribute::*，获取第 1个 li 结点的所有属性
            - 除了上述关键字，还有 child:: 所有直接子节点； descendant:: 所有子孙结点。   
    '''
    html = etree.parse('test.html', etree.HTMLParser())     # 网页文本解析为一个 xpath 可处理的对象。进行补齐 闭合 tag，
    # 添加 <body>, <html> <!DOCTYPE > 标签等工作
    result = etree.tostring(html)
    print(result.decode('utf-8'))      # byte 格式，decode 为 文本形式

    result1 = html.xpath('//*')  # '//' 表示从当前节点选取子孙结点。 ‘//*’ 表示匹配所有结点
    print(result1)

    result2 = html.xpath('//li')  # 获取所有 li 结点 [<Element li at 0x24b61488300>, <Element li at 0x24b61488380>, ...]
    print(result2)

    res3 = html.xpath('//li/a')  # '/' 单斜线表示 直接子节点; 而 '//' 表示的是 子孙结点-即不一定要为直接子节点，可以为多层子节点
    print(res3)

    # a href="//search.sohu.com/?keyword=人才&queryType=outside"
    # 演示 父节点的使用，以及 特定属性标签的选取 和 属性值的获取
    res4 = html.xpath('//a[@href="//search.sohu.com/&queryType=outside"]/../@data-tag-id')  # 删除中文字符后可以匹配。中文字符匹配不行。
    print(res4)  # 输出： ['77953']， 获取到对应的 id值

    res5 = html.xpath('//a[@href="//search.sohu.com/&queryType=outside"]//text()')  # text() 函数获取tags 之间的文本
    print(res5)   # 返回： ['test!!']

    res6 = html.xpath('//li[2]/a/text()')  # li[2]  表示获取第二个 li 节点
    print(res6)
