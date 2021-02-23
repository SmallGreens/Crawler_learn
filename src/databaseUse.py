"""
介绍使用 python 将爬取的内容保存到 文件。
    就是各种存储方式的应用。 -- 之前没有了解过 MongoDB， 在这里顺便了解一下。

"""
import csv
import json
import re
import pymysql
import pymongo
import chardet
import requests
from bs4 import BeautifulSoup as bs


def get_html(url):
    """获取网页内容并保存到文件中"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:85.0) Gecko/20100101 Chrome/70.5'}
    html = requests.get(url, headers=headers)
    with open('html_file.txt', 'w', encoding='utf-8') as f:
        f.write(html.text)


def write_to_txt(file_name, soup):
    """
    写入到 文件中。
    参数：'a', 在结尾添加，参数 ‘w’ 表示写入，如果存在，覆盖内容
    """
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write("测试例子\n")

    with open(file_name, 'a', encoding='utf-8') as f:
        for item in soup.find_all('h4'):
            if item.string is not None:
                f.write(item.string)
                f.write('\n')


def connect_mysql():
    '''
    使用 python 连接数据库需要首先安装 连接工具： pymysql
    official docu: https://pymysql.readthedocs.io/en/latest/
    pip install pymysql
    '''
    db = pymysql.connect(host='localhost', user='root', passwd='root', port=3306, db='spider')  # host 传入 ip 地址，这里使用本地测试
    cursor = db.cursor()   # 获取 mysql 的操作游标，便可以使用它来执行数据库指令
    cursor.execute('SELECT VERSION()')
    data = cursor.fetchone()
    print('The version of database: ', data)  # '5.7.31-log'
    # cursor.execute('CREATE SCHEMA `spider` DEFAULT CHARACTER SET utf8')
    """
    创建 table 
    sql = '''
    CREATE TABLE IF NOT EXISTS `spider`.`test` (
        `id` VARCHAR(255) NOT NULL,
        `name` VARCHAR(255) NOT NULL,
        `age` INT NOT NULL,
    PRIMARY KEY (`id`));
    '''
    cursor.execute(sql)
    """
    sql = 'INSERT INTO test(id, name, age) values(%s, %s, %s)'
    id = '12345'
    name = 'xiaoMing'
    age = '20'
    try:
        cursor.execute(sql, (id, name, age))
        db.commit()
    except Exception:
        db.rollback()
    db.close()


def main1():
    # get_html('https://xueqiu.com/7431373305/172472683')
    html_file = open('html_file.txt', 'r', encoding='utf-8')
    soup = bs(html_file, 'lxml')
    print(soup.prettify())
    # write_to_txt(file_name='xueqiu_doc.txt', soup=soup)
    print('*' * 40)
    reg = re.compile('window.SNOWMAN_STATUS.*')
    st = ''
    '''
    存储为 json 对象。
        下面例子中，从html 中提取 json 对象，并转为 python 中的 dict 对象
    '''
    for item in soup.find_all('script'):
        # 这里 虽然 item.string 的类型是 str 的子类，但是还是会报类型错误，必须 str() 函数 进行转换后才能运行
        if re.match(reg, str(item.string)) is not None:
            st = item.string
    j = re.search('{"id".*}', st, re.S).group(0)
    json_obj = json.loads(j)
    print(type(json_obj))
    print(json_obj.get('text'))

    '''
    CSV 存储 - csv 全称为 comma-Separated values. 中文可以叫做 逗号分隔值 或 字符分隔值， 其 文件以纯文本的形式存储
    python 中提供内置库来处理 csv 文件
    
    此外，一些数据分析库，例如 pandas，亦提供了 
    '''
    with open('data.csv', 'w') as csv_file:
        writer = csv.writer(csv_file, delimiter=' ')  # 设置每行元素之间的间隔，这里修改为了 空格（默认为逗号）
        # writer = csv.DictWriter() -- csv 提供字典写入工具，将 python 中的 字典对象写入
        writer.writerow(['id', 'name','age'])
        writer.writerow(['1234', 'xiaoMing', 20])
        writer.writerow(['1235', 'xiaoFang', 25])


if __name__ == '__main__':
    '''
    MongoDB: mongoDB 是由 C++ 编写的非关系型数据库，是一个基于分布式文件存储的开源数据库系统。
    其内容存储形式类似 json 对象，它的字段值可以包含其他文档、数组、以及文档数组， 使用非常灵活。
    
    MongoDB 的安装： https://www.runoob.com/mongodb/mongodb-window-install.html
    我将 mongodb 安装在了 'D:\MongoDB'. 网上很多教程介绍了一堆配置。
    但是看了下官网的文档，似乎 通过 在 安装时选择 将 mongoDB 作为一个 service，安装完毕后它就会自动在系统中启动 mongoDB 服务。
    link: https://docs.mongodb.com/manual/tutorial/install-mongodb-on-windows/
    
    因此，我直接仅仅安装了软件，没有做任何配置。下述的操作皆可以正常运行。 
    
    使用 python 连接 mongodb 使用 pymongo：https://pymongo.readthedocs.io/en/stable/
    pip install pymongo
    '''
    # step1: 连接数据库
    client = pymongo.MongoClient(host="localhost", port=27017)
    # step2：指定数据库
    db = client.test
    # step3：指定集合
    # mongodb 中，每个数据库包含很多集合（collection），他们类似于关系型数据库中的表
    collection = db.students
    collection.delete_many({})  # 清空集合中的数据
    student = {
        'id': '11111',
        'name': 'XiaoMing',
        'age': 20,
        'gender': 'male'
    }
    student1 = {
        'id': '11112',
        'name': 'XiaoGang',
        'age': 26,
        'gender': 'male'
    }
    student2 = {
        'id': '11113',
        'name': 'XiaoTing',
        'age': 27,
        'gender': 'female'
    }
    # insert is deprecated. Use insert_one or insert_many instead.
    res = collection.insert_one(student)  # insert_one, 插入一条数据， insert_many 插入多条数据
    res1 = collection.insert_many([student1, student2])  # insert_many, 需要传入一个 list
    print(res)
    print(res1)

    # step4: 查询数据
    res2 = collection.find_one({'name':'XiaoGang'})  # 传入一个 map
    print(res2)  # {'_id': ObjectId('xx'), 'id': '11112', 'name': 'XiaoGang', 'age': 26, 'gender': 'male'}
    res3 = collection.find({'gender': 'male'})   # find 查询多条数据
    print(res3)  # 返回一个 pymongo.cursor.Cursor 对象
    for stu in res3:
        print(stu)
    res4 = collection.find({'age': {'$gt': 20}})   # 查找年龄大于 20 的同学 -- $gt：大于；$lt：小于；$lte: 小于等于；$gte: 大于等于
    for i in res4:
        print(i)
    res5 = collection.find({'name':{'$regex': '-*?T.*'}})
    for i in res5:
        print('with t: ', i)






