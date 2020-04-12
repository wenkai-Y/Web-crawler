# 电影天堂
from lxml import etree
import requests

BASE_DOMAIN = 'https://www.dytt8.net'
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/81.0.4044.92 Safari/537.36 ',
    'Referer': 'https://www.dytt8.net/html/gndy/dyzz/list_23_1.html'
}


def get_detail_urls(url):
    response = requests.get(url, headers=HEADERS)
    # response.text
    # response.content
    # response库会默认使用自己猜测的编码方式进行解码，储存在text中，而编码方式错误
    text = response.content.decode(encoding='GBK', errors='ignore')
    html = etree.HTML(text)
    detail_urls = html.xpath("//table[@class='tbspan']//a/@href")
    detail_urls = map(lambda urls: BASE_DOMAIN + urls, detail_urls)
    return detail_urls


def parse_detail_page(url):
    movie = {}
    response = requests.get(url, headers=HEADERS)
    text = response.content.decode('gbk')
    html = etree.HTML(text)
    title = html.xpath("//div[@class='title_all']//font[@color='#07519a']/text()")[0]
    # 电影标题
    movie['title'] = title
    zoomE = html.xpath("//div[@id='Zoom']")[0]
    cover = zoomE.xpath(".//img/@src")
    # 电影截图
    movie["cover"] = cover
    infos = zoomE.xpath(".//text()")
    for index, info in enumerate(infos):
        if info.startswith("◎年　　代"):
            info = info.replace("◎年　　代", "").strip()
            movie["year"] = info
        elif info.startswith("◎产　　地"):
            info = info.replace("◎产　　地", "").strip()
            movie["country"] = info
        elif info.startswith("◎类　　别"):
            info = info.replace("◎类　　别", "").strip()
            movie["category"] = info
        elif info.startswith("◎豆瓣评分"):
            info = info.replace("◎豆瓣评分", "").strip()
            movie["movie_rating"] = info
        elif info.startswith("◎片　　长"):
            info = info.replace("◎片　　长", "").strip()
            movie["times_long"] = info
        elif info.startswith("◎主　　演"):
            info = info.replace("◎主　　演", "").strip()
            actors = [info]
            for x in range(index + 1, len(infos)):
                actor = infos[x].strip()
                if actor.startswith("◎标　　签"):
                    break
                actors.append(actor)
            movie['actors'] = actors
        elif info.startswith("◎简　　介"):
            info = info.replace("◎简　　介", "").strip()
            profiles = [info]
            for x in range(index + 1, len(infos)):
                profile = infos[x].strip()
                if profile.startswith("【下载地址】"):
                    break
                profiles.append(profile)
                while "" in profiles:
                    profiles.remove("")
            movie['profiles'] = profiles
    download_url = html.xpath("//td[@bgcolor='#fdfddf']//a/@href")
    movie["download_url"] = download_url
    return movie


def spider():
    base_url = 'https://www.dytt8.net/html/gndy/dyzz/list_23_{}.html'
    movies = []
    for x in range(1, 2):
        # 控制
        url = base_url.format(x)
        detail_urls = get_detail_urls(url)
        for detail_url in detail_urls:
            # 遍历详情
            movie = parse_detail_page(detail_url)
            movies.append(movie)
    # 输出数组
    print(movies)


if __name__ == '__main__':
    spider()
