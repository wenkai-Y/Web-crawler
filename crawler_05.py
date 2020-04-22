# 古诗文网
import re
import requests

HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/81.0.4044.113 Safari/537.36 ",
    "referer": "https://www.gushiwen.org/default_2.aspx",
    "cookie": "login=flase"
}
POEMS = []

TITLE = re.compile('<div\sclass="cont">.*?<b>(.*?)</b>', re.DOTALL)
DYNASTY = re.compile(r'<div\sclass="cont">.*?<p\sclass="source">.*?<a\s.*?target="_blank">(.*?)</a>', re.DOTALL)
AUTHOR = re.compile(r'<div\sclass="cont">.*?<p\sclass="source">.*?<span>：</span>.*?<a\s.*?target="_blank">(.*?)</a>',
                    re.DOTALL)
CONTENT = re.compile(r'<div\sclass="contson"\s.*?>(.*?)</div>', re.DOTALL)
CHANGE = re.compile(r'<.*?>')


def parse_page(url):
    response = requests.get(url, headers=HEADERS)
    text = response.text
    # 正则表达式解析
    # .号不能匹配反斜杠\n
    # 匹配所有的字符
    # 标题
    titles = re.findall(TITLE, text)
    dynasties = re.findall(DYNASTY, text)
    authors = re.findall(AUTHOR, text)
    controls_N = re.findall(CONTENT, text)
    controls = []
    for control in controls_N:
        # 替换字符
        control = re.sub(CHANGE, "", control).split()[0]
        # 导入字符串
        controls.append(control)
    for value in zip(titles, dynasties, authors, controls):
        # 解包
        title, dynasty, author, control = value
        poem = {
            "title": title,
            "dynasty": dynasty,
            "author": author,
            "control": control
        }
        POEMS.append(poem)


def main():
    url = "https://www.gushiwen.org/default_{}.aspx"
    for x in range(1, 11):
        parse_page(url.format(x))
    for poem in POEMS:
        print(poem)
        print("*"*100)


if __name__ == '__main__':
    main()
