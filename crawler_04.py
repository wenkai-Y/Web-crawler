# 豆瓣网
import requests
from lxml import etree

movies = []

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.113 Safari/537.36 ',
    'Referer': 'https://movie.douban.com/'
}

url = 'https://movie.douban.com/cinema/later/xian/'

response = requests.get(url, headers=headers)
text = response.text

html = etree.HTML(text)

divs_showing = html.xpath("//div[@id='showing-soon']")
div_showing = divs_showing[0]
div_items = div_showing.xpath("./div")

# 循环
for div_item in div_items:
    div_intro = div_item.xpath("./div[@class='intro']")[0]
    lis = div_intro.xpath("./ul/li")
    # 电影名字
    name = div_intro.xpath("./h3/a/text()")[0]
    # 电影链接
    url = div_intro.xpath("./h3/a/@href")[0]
    # 图片地址
    image = div_item.xpath("./a/img/@src")[0]
    # 电影开影日期
    date_showing = "2020年 " + lis[0].xpath("./text()")[0]
    # 电影类型
    types = lis[1].xpath("./text()")[0]
    # 制作地区
    county = lis[2].xpath("./text()")[0]
    # 多少人想看
    peoples = lis[3].xpath(".//text()")[0]
    movies.append({
        "电影名称": name,
        "电影链接": url,
        "图片": image,
        "开映日期": date_showing,
        "电影类型": types,
        "电影产地": county,
        "期待数": peoples
    })

for movie in movies:
    print(movie)
