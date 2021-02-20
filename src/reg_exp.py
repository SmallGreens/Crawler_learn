import re

if __name__ == '__main__':
    '''
    介绍 python 正则表达式的使用
        - 用途：主要用于字符串的 检索、替换 等工作。
        - 工具：正则表达式测试： https://tool.oschina.net/regex/ -- 该网站还提供常用的正则表达式，例如 邮箱匹配，电话号码，qq号，身份证等
        - python 库：python中的 re 库提供了正则表达式的功能实现。
        
    re 库中使用 regex 的技巧：
        - .* 匹配任意数量的字串
        - () 需要从匹配到的字串中提取部分内容，使用小括号将这部分内容括起来
        - .*? 为非贪婪模式，可以匹配尽量少的字串， （.* 为贪婪模式）
        - . 可以匹配除换行外的任意字符，如果希望也能匹配换行，在匹配方法中添加修饰符：re.S. (常用的修饰符还有 re.I 不区分大小写)
    
    re 库中的方法
        - match() 方法
            - 从头开始匹配 content 和 正则表达式（如果开头不匹配，立即匹配失败）， 返回一个 re.Match 对象记录匹配结果
            - 适合检查一个子串是否满足某个正则表达式的格式要求
        - search() 方法
            - 扫描整个输入内容，返回第一个匹配成功的结果
            - 适合查找一段内容中 是否含有 某一特定信息
        - findall() 方法
            - 扫描整个输入内容，返回所有匹配的结果
            - 返回为一个列表，每个列表元素为一个元组（tuple），包含 ‘()’ 所指定的提取内容
        - sub() 方法
            - 使用正则表达式替换输入内容中的特定内容， re.sub('regex', '替换内容'， content)
        - compile() 方法
            - 可以将正则表达式包装成一个对象
            - 语法： pattern = re.compile('regex')
    '''
    content = 'hello 123'
    regex = r'^hello\s\d{3}'  # ‘^hello’ 表示以 hello 开头， ’\s‘ 表示空格， ‘\d{3}’ 表示 匹配3个数字
    res = re.match(regex, content)
    print(res)  # <re.Match object; span=(0, 9), match='hello 123'>，
    # 结果是 re.Match 对象， span(0, 9) 表示匹配的范围，为在原字符串中的位置信息
    print(res.group())  # group() 方法返回匹配到的 内容

    regex1 = r'^hello\s(\d{3})'   # 如果需要提取匹配得到的内容中的一部分内容， 使用括号将该部分内容包起来，
    res1 = re.match(regex1, content)
    print(res1.group(1))  # 返回第一个 括号中的内容：'123', 同理， group(2) 返回第二个括号中的内容

    content1 = 'test hahaha xxxx 123 hh last'
    regex2 = '^test.*last$'    #  使用 '.*' ‘。’ 可以匹配任意字符（除换行）， ‘*’ 则表示匹配任意次数
    res2 = re.match(regex2, content1)
    print(res2.group())  # 输出： test hahaha xxxx 123 hh last

    regex3 = r'^test.*(\d+).*last$'
    res3 = re.match(regex3, content1)
    print(res3.group(1))   # 输出： 3, ’.*‘ 为贪婪模式，会匹配尽可能多的字串

    regex4 = r'^test.*?(\d+).*last$'
    res4 = re.match(regex4, content1)
    print(res4.group(1))  # 输出： 123，  '.*?' 为非贪婪模式，匹配尽可能少的字串。 -- 通常推荐使用非贪婪模式。但是在字符串尾部时，需要小心使用，因为可能无法匹配到任何字串

    content2 = '''hello 
    world'''
    regex5 = r'^hello.*?(\w+)'
    res5 = re.match(regex5, content2, re.S)  # 需要添加修饰符， re.S, 才能让 '.' 匹配到换行符
    print(res5.group(1))   # 输出： world
