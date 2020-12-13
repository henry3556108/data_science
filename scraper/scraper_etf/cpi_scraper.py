from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
# import requests
import time
from os import makedirs
import os


class CPI_creater():
    def __init__(self):
        self.browser = None

    def __CPI_rate_filter(self,df):
            # df = pd.read_csv("test.csv", index_col= 0)
            df.columns = ["year", "01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
            # 把不要的第一行砍掉
            df = df.dropna()
            # 整理一下 index
            df = df.reset_index(drop = True)
            # 尋找最後面的那個 2010 從這個 row 之後就是我們要的資料
            start = int(df[df["year"]=="2010"].index[-1])
            # print(start)
            df = df.iloc[start:]
            return df

    def init_browser(self):
        if self.browser != None:
            self.browser.close()
        options = webdriver.ChromeOptions()
        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        options.add_argument('user-agent={}'.format(agent))
        options.add_argument("--headless")
        self.browser = webdriver.Chrome(options=options)

    def get_CPI_data(self):
        self.init_browser()
        href = "https://www.bls.gov/regions/mid-atlantic/data/consumerpriceindexhistorical_us_table.htm"
        self.browser.get(href)
        tables = self.browser.find_elements_by_tag_name("table")
        
        # 第一個表會是 CPI-U 第二個表會是 CPI-W
        CPIU = pd.read_html(tables[0].get_attribute("outerHTML"))[0]
        CPIW = pd.read_html(tables[1].get_attribute("outerHTML"))[0]
        
        CPIU = self.__CPI_rate_filter(CPIU)
        CPIW = self.__CPI_rate_filter(CPIW)
        return CPIU, CPIW
        


def main():
    creater = CPI_creater()
    cpiu, cpiw = creater.get_CPI_data()
    cpiu.to_csv("CPIU.csv")
    cpiw.to_csv("CPIW.csv")

if __name__ == "__main__":
    main()
