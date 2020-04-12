# 中国天气网
import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Bar

ALL_DATA = []


def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/81.0.4044.92 Safari/537.36 '
    }
    response = requests.get(url, headers=headers)
    text = response.content.decode('UTF-8')
    # 解析数据
    soup = BeautifulSoup(text, 'html5lib')
    conMidtab = soup.find('div', class_='conMidtab')
    tables = conMidtab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-2]
            min_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({"city": city, "min_temp": int(min_temp)})
            # print({"城市": city, "最低气温": int(min_temp)})


def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        "http://www.weather.com.cn/textFC/hz.shtml",
        "http://www.weather.com.cn/textFC/hn.shtml",
        "http://www.weather.com.cn/textFC/xb.shtml",
        "http://www.weather.com.cn/textFC/xn.shtml",
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]
    for url in urls:
        parse_page(url)
    # 分析数据
    # 根据最低气温进行排序
    ALL_DATA.sort(key=lambda data: data['min_temp'])
    # print(ALL_DATA)
    data = ALL_DATA[0:10]
    # pyecharts 可视化
    # chart = Bar()
    cities = []
    temps = []
    for city_temp in data:
        cities.append(city_temp["city"])
        temps.append(city_temp['min_temp'])
    bar = (
        Bar().add_yaxis("最低气温", temps).add_xaxis(cities)
    )
    bar.render('temperature.html')


if __name__ == '__main__':
    main()

