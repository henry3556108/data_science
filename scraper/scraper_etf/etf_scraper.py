from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


class ETF_scraper:
    def __init__(self):
        self.browser = None
        self.period2 = "2095980800"

    def init_browser(self):
        if self.browser != None:
            self.browser.close()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        # agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        # options.add_argument('user-agent={}'.format(agent))
        self.browser = webdriver.Chrome(options=options)

    def time_parser(self, data):
        try:
            weekday_map = {"Dec": "12", "Nov": "11", "Oct": "10", "Sep": "09", "Aug": "08",
                           "Jul": "07", "Jun": "06", "May": "05", "Apr": "04", "Mar": "03", "Feb": "02", "Jan": "01"}
            date = data["date"].replace(",", "")
            date = date.split(" ")
            date[0] = weekday_map[date[0]]
            date[0], date[1], date[2] = date[2], date[0], date[1]
            data["date"] = "".join(date)
            return data
        except:
            return ""

    def __filter(self, x):
        if x[1] == x[2] == x[3] == x[4]:
            False
        else:
            return True

    def format_data(self, df, name):
        df = df[df.apply(lambda x: self.__filter(x), axis=1)
                == True] if "%5E" not in name else df
        try:
            df = df.drop(["Adj Close**"], axis=1)
            df.columns = ["date", "open", "high", "low", "close", "volume"]
            df = df.apply(self.time_parser, axis=1)
        except:
            pass

        return df

    def get_ETF_history(self, name):
        self.init_browser()
        yahooHref = f"https://finance.yahoo.com/quote/{name}/history?period1=631238400&period2={self.period2}&interval=1d&filter=history&frequency=1d"
        try:
            self.browser.get(yahooHref)
            for i in range(1, 300):
                self.browser.execute_script(f"window.scrollTo(0, {i*1000});")
            df = pd.read_html(self.browser.find_element_by_tag_name(
                "table").get_attribute("outerHTML"))
            return self.format_data(df[0], name)

        except:
            print(f"something wrong in {name}")


    def get_etf_db_data(self, etf_db_url):
        self.init_browser()
        self.browser.get(etf_db_url)
        df = pd.read_html(self.browser.find_element_by_tag_name(
            "table").get_attribute("outerHTML"))
        pass

    def get_ETF_holding(self):
        self.init_browser()
        pass


def main():
    creater = ETF_scraper()
    ls = []
    # ls = ["%5EDJI"]
    # ls = [ "EFA", "IEMG", "VEA", "XLF", "HYG"]
    # ["SPY", "QQQ", "IVV", "EEM", "VTI", "XLF", "VTV", "USO","GLD", "GDX", "VOO",
    for etf in ls:
        df = creater.get_ETF_history(etf)
        name = etf if "%5E" not in etf else etf.replace("%5E", "")
        df.to_csv(f"{name}.csv", index=None)
    
if __name__ == "__main__":
    main()
