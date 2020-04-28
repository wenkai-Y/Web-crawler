from selenium import webdriver
# 引入等待
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class QiangPiao(object):
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.login_url = 'https://kyfw.12306.cn/otn/resources/login.html'
        self.initmy_url = "https://kyfw.12306.cn/otn/view/index.html"
        self.order_url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc'

    def _login(self):
        self.driver.get(self.login_url)
        # 显示等待(一直)（建议）
        WebDriverWait(self.driver, 60).until(
            EC.url_to_be(self.initmy_url)
        )
        print("登录成功")
        # 隐式等待（有时间限制）（不建议）

    def _wait_input(self):
        self.from_station = input("请输入起始站：")
        self.to_station = input("请输入终点站：")
        # 实践格式必须正确：yyyy-mm-dd
        self.depart_time = input("请输入出发时间：")
        self.passengers = input("请输入乘车人").split(',|，')
        self.trans = input("请输入车次：")

    def _order_ticket(self):
        # 1.跳转到首页
        self.driver.get(self.order_url)
        # 2.等待出发地是否输入正确
        WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element_value((By.ID, "fromStationText"), self.from_station)
        )
        # 3.等待目的地是否输入正确
        WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element_value((By.ID, "toStationText"), self.to_station)
        )
        # 4.等待出发日期是否输入正确
        WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element_value((By.ID, "train_date"), self.depart_time)
        )
        # 5.等待查询按钮是否可用
        WebDriverWait(self.driver, 60).until(
            EC.element_to_be_clickable((By.ID, "query_ticket"))
        )
        # 6.如果可以被点击了，则找到查询按钮，执行点击事件
        searchBtn = self.driver.find_element_by_id('query_ticket')
        searchBtn.click()

    def run(self):
        self._wait_input()
        self._login()
        self._order_ticket()


if __name__ == '__main__':
    spider = QiangPiao()
    spider.run()
