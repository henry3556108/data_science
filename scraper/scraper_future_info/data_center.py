import pandas as pd
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import random
import datetime


class Data_center():
    def __init__(self):
        self.pcr_url = "https://www.taifex.com.tw/cht/3/pcRatio"
        self.fxf_url = ""
        self.exf_url = ""
        self.txf_url = ""
        self.browser = None

    def init_browser(self, hide=True):
        '''
        init browser, if you want to see what I do, you can change hide value to False
        '''
        options = webdriver.ChromeOptions()
        if hide:
            options.add_argument("--headless")
        agent = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.{random.randint(0, 255)} Safari/537.36"
        options.add_argument('user-agent={}'.format(agent))
        self.browser = webdriver.Chrome(options=options)

    def _get_date(self, start_date: str, end_date: str) -> tuple:
        '''
        會回傳一連串的日期，從start_date到end_date，並且都間隔 30 日
        '''
        start_date = datetime.datetime.strptime(start_date, "%Y/%m/%d")
        end_date = datetime.datetime.strptime(end_date, "%Y/%m/%d")
        date_delta = (end_date - start_date).days
        dates = []
        if date_delta == 0:
            dates = [(f"{start_date.year}/{start_date.month}/{start_date.day}",
                      f"{start_date.year}/{start_date.month}/{start_date.day}")]
        while date_delta > 0:
            tmp_delta = 30 if date_delta >= 30 else date_delta
            # print()
            current_end = start_date + datetime.timedelta(tmp_delta)

            dates.append((f"{start_date.year}/{start_date.month}/{start_date.day}",
                          f"{current_end.year}/{current_end.month}/{current_end.day}"))

            start_date += datetime.timedelta(tmp_delta + 1)
            date_delta -= (tmp_delta + 1)
        return dates

    def get_pcr(self, start_date = "2010/1/1", end_date = "2010/12/31") -> pd.DataFrame:
        '''
        從台灣證交所上面，抓下日期間的 PCR
        '''
        self.init_browser()
        self.browser.get(self.pcr_url)
        pcr_df = pd.DataFrame()
        dates = self._get_date(start_date, end_date)
        for start, end in dates:
            start_tag = self.browser.find_element_by_name("queryStartDate")
            end_tag = self.browser.find_element_by_name("queryEndDate")
            start_tag.clear()
            end_tag.clear()
            start_tag.send_keys(start)
            end_tag.send_keys(end)

            send_buttom = self.browser.find_element_by_name("button3")
            send_buttom.click()
            html = self.browser.execute_script(
                "return document.documentElement.outerHTML")
            soup = BeautifulSoup(html)
            table = soup.find("table", {"class": "table_a"})
            df = pd.read_html(table.prettify())
            pcr_df = pd.concat([pcr_df, df[0]])
            
        pcr_df["日期"] = pcr_df["日期"].apply(lambda x : pd.to_datetime(x, format="%Y/%m/%d"))
        pcr_df = pcr_df.sort_values("日期")
        pcr_df = pcr_df.reset_index(drop = True)
        return pcr_df
        

def get_data(file_name: str) -> pd.DataFrame:
    if file_name.endswith(".csv"):
        df = pd.read_csv(file_name)
    return df


if __name__ == "__main__":
    center = Data_center()
    center.get_pcr()
