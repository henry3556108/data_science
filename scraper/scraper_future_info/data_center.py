import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
# from seleniumrequests import Chrome
class Data_center():
    def __init__(self):
        self.pcr_url = "https://www.taifex.com.tw/cht/3/pcRatio"
        self.fxf_url = ""
        self.exf_url = ""
        self.txf_url = ""
        self.browser = None

    def init_browser(self, hide = True):
        options = webdriver.ChromeOptions()
        if hide :
            options.add_argument("--headless")
        agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.{random.randint(0, 255)} Safari/537.36"
        options.add_argument('user-agent={}'.format(agent))
        self.browser = webdriver.Chrome(options=options)

    def get_pcr(self):
        self.init_browser()
        self.browser.get(self.pcr_url)
        start_tag = self.browser.find_element_by_name("queryStartDate")
        end_tag = self.browser.find_element_by_name("queryEndDate")
        
        # dates = _get_dates()

        start_tag.clear()
        end_tag.clear()
        start_tag.send_keys("2010/9/1")
        end_tag.send_keys("2010/9/30")
        
        send_buttom = self.browser.find_element_by_name("button3")
        send_buttom.click()
        html = self.browser.execute_script("return document.documentElement.outerHTML")
        soup = BeautifulSoup(html)
        table = soup.find("table", {"class": "table_a"})
        df = pd.read_html(table.prettify())
        df[0].head()
        print()


def get_data(file_name : str) -> pd.DataFrame:
    if file_name.endswith(".csv"):
        df = pd.read_csv(file_name)
    return df





if __name__ == "__main__":
    center = Data_center()
    center.get_pcr()
    # df = get_data(file_name = "raw_data/EXF1-分鐘-成交價.csv")
    # f = requests.get("/down_type=&queryStartDate=2020%2F12%2F06&queryEndDate=2021%2F01%2F05")
    # print(f.text)
    # d = {'down_type':'', 'queryStartDate': '2010%2F12%2F06', 'queryEndDate': '2010%2F01%2F05'}
    # df = pd.read_html("https://www.taifex.com.tw/cht/3/pcRatio")
    # print(df[0].head())
    # url = 'https://www.taifex.com.tw/cht/3/pcRatio'
    # header = {"Sec-Fetch-Dest": "document", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    # url = 'https://www.taifex.com.tw/cht/3/pcRatio'

    # respone = driver.request("POST", url,  data = d)
    # # table = driver.find_element_by_tag_name("table")
    # # print()
    # # print(df.head())
    # # r = requests.post(url, data=d, headers = header)
    # soup = BeautifulSoup(respone.text)
    # # # soup = soup.prettify()
    # for tr in soup.findAll("tr"):
    #     print(tr.text)
    # print(soup)
    # print(r.text)
    # print(df.head())