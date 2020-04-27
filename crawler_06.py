# 拉勾网爬取ajax数据

"""方法一：分析接口获取json数据"""
# import requests
# import time
# from lxml import etree
#
# HEADERS = {
#     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                   "Chrome/81.0.4044.113 Safari/537.36 ",
#     "referer": "https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=",
#     "cookie": "user_trace_token=20200414194740-21b70e4b-955d-498e-bff4-81305c707787; "
#               "LGUID=20200414194740-6da52ffe-62ed-4e36-a2a5-31fb61734306; _ga=GA1.2.1543321299.1586864861; "
#               "sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221717884a3aa237-05a77ec6927369-87f133f-1350728"
#               "-1717884a3abac5%22%2C%22%24device_id%22%3A%221717884a3aa237-05a77ec6927369-87f133f-1350728"
#               "-1717884a3abac5%22%7D; index_location_city=%E4%B8%8A%E6%B5%B7; "
#               "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1586864862,1586864896,1587912910; "
#               "_gid=GA1.2.946822281.1587912910; JSESSIONID=ABAAABAABEIABCI040512DE6EA1D9BC48889DCD3D121697; "
#               "WEBTJ-ID=20200427142901-171ba531d815d5-0778fa50ec4f06-6373664-1350728-171ba531d822ca; "
#               "X_HTTP_TOKEN=f8fed4315e22a34f149869785139dacbe3acb9f947; PRE_UTM=; "
#               "PRE_LAND=https%3A%2F%2Fwww.lagou.com%2F; LGSID=20200427142901-2b94e011-fa78-4311-9266-c463f878de51; "
#               "PRE_HOST=cn.bing.com; PRE_SITE=https%3A%2F%2Fcn.bing.com%2F; TG-TRACK-CODE=search_code; _gat=1; "
#               "LGRID=20200427145600-12539136-08e9-43a7-8344-5a2a55ab36fb; SEARCH_ID=9362b744bca8417bafa23fa6cc335f85",
#     "x-anit-forge-code": "0",
#     "x-anit-forge-token": "None",
#     "x-requested-with": "XMLHttpRequest",
#     "origin": "https://www.lagou.com"
#
# }
# DATA = {
#     'first': 'false',
#     'pn': 1,
#     'ks': 'python'
# }
#
#
# def request_list_page():
#     url = "https://www.lagou.com/jobs/positionAjax.json?city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false"
#     # 获取几页
#     for x in range(1, 5):
#         DATA["pn"] = x
#         response = requests.post(url, data=DATA, headers=HEADERS)
#         # print(response.json())
#         result = response.json()
#         # 列表
#         # print(result)
#         positions = result['content']['positionResult']['result']
#         for position in positions:
#             print(position)
#             positionID = position['positionId']
#
#         break
#
#
# def main():
#     request_list_page()
#
#
# if __name__ == '__main__':
#     main()


"""方法二：利用selenium获取信息"""
from selenium import webdriver
import time
import re


class LagouSpider(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.url = "https://www.lagou.com/jobs/list_python/p-city_3?&cl=false&fromSearch=true&labelWords=&suginput="
        self.position = []

    def run(self):
        self.driver.get(self.url)
        geiyebuhao = self.driver.find_element_by_class_name('body-btn')
        geiyebuhao.click()
        while True:
            source = self.driver.page_source
            self.parse_list_page(source)
            nextTag = self.driver.find_element_by_xpath('//div[@class="pager_container"]/span[last()]')
            if "pager_next_disabled" in nextTag.get_attribute("class"):
                break
            else:
                nextTag.click()
            time.sleep(2)
        self.driver.quit()
        for position in self.position:
            print(position)

    def parse_list_page(self, source):
        hrefs_1 = re.findall(r'<div\sclass="p_top">.*?<a\sclass="position_link"\shref="(.*?)".*?>', source, re.DOTALL)
        hrefs = hrefs_1[0:-2]
        for href in hrefs:
            self.request_detail_page(href)
            time.sleep(3)

    def request_detail_page(self, url):
        self.driver.execute_script("window.open('{}')".format(url))
        self.driver.switch_to.window(self.driver.window_handles[-1])
        source = self.driver.page_source
        self.parse_detail_page(source)
        time.sleep(3)
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])

    def parse_detail_page(self, source):
        position_name = re.findall(r'<h1\sclass="name">(.*?)</h1>', source, re.DOTALL)[0]
        # print(position_name)
        job_request = re.findall(r'<dd\sclass="job_request">.*?<h3>(.*?)</h3>', source, re.DOTALL)[0]
        salary = re.findall(r'<span\sclass="salary">(.*?)</span>', job_request, re.DOTALL)[0]
        request_job = re.findall(r'<span>(.*?)</span>', job_request, re.DOTALL)
        city = re.sub(r'/|\s/|\s/', '', request_job[0])
        ask = ''
        for aski in request_job[1:]:
            ask += aski
        ask = re.sub(r'/|\s/|/\s', '', ask)
        position = {
            "职业名称": position_name,
            "城市": city,
            "薪酬": salary,
            "工作要求": ask
        }
        self.position.append(position)


if __name__ == '__main__':
    spider = LagouSpider()
    spider.run()
