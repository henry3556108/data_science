from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


class ETFDB_center:
    def __init__(self):
        self.browser = None
        self.period2 = "2095980800"

    def init_browser(self):
        if self.browser != None:
            self.browser.close()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
        options.add_argument('user-agent={}'.format(agent))
        self.browser = webdriver.Chrome(options=options)

    def get_etf_db_data(self, etf_db_url, sort_condition = None, top=30):
        df = pd.DataFrame()
        for i in range(1, 30):

            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
            options.add_argument('user-agent={}'.format(agent))
            browser = webdriver.Chrome(options=options)
            url = etf_db_url.format(page = i) if sort_condition == None else etf_db_url.format(page = i, sort = sort_condition)
            browser.get(url)
            print(url)
            dfs = pd.read_html(browser.find_element_by_tag_name(
                "table").get_attribute("outerHTML"))

            dfs[0] = dfs[0].drop([dfs[0].index[-1]])
            df = pd.concat([df, dfs[0]])
            browser.close()
            if len(df.index) > top:
                break
        df = df.reset_index()
        df = df.head(top)
        return df


def main():
    creater = ETFDB_center()
    # https://etfdb.com/screener/#page=1&sort_direction=desc&sort_by=price
    # https://etfdb.com/screener/#page=1&sort_by=price&sort_direction=desc
    sort_conditions = {
                    #    "price": "&sort_by=price",
                    #    "avg_volume": "&sort_by=average_volume",
                    #    "ytd": "sort_direction=desc&sort_by=ytd",
                    #    "beta": "sort_direction=desc&sort_by=beta",
                       "beta":"&sort_by=beta&sort_direction=desc", 
                    #    "standard_deviation":"&sort_by=standard_deviation&sort_direction=desc"
                       }
    urls = {
        # "Large_Cap_Value":"https://etfdb.com/screener/#page={page}{sort}&asset_class=equity&sizes=Large-Cap&investment_strategies=Value&sort_direction=desc",
        # "Large_Cap_Growth":"https://etfdb.com/screener/#page={page}{sort}&asset_class=equity&sizes=Large-Cap&investment_strategies=Growth&sort_direction=desc",
        # "Large_Cap_Value" : "https://etfdb.com/screener/#page={page}{sort}&asset_class=equity&sizes=Large-Cap&investment_strategies=Value",
    #         "Large_Cap_Growth" : "https://etfdb.com/screener/#page={}{}&asset_class=equity&sizes=Large-Cap&investment_strategies=Growth",
        # "Small_Cap" : "https://etfdb.com/screener/#page={page}&sort_direction=desc{sort}&asset_class=equity&sizes=Small-Cap",
            # "Mid_Cap" : "https://etfdb.com/screener/#page={page}&sort_direction=desc{sort}&asset_class=equity&sizes=Mid-Cap",
            # "Bond_Long_Term" : "https://etfdb.com/screener/#page={page}{sort}&sort_direction=desc&asset_class=bond&bond_duration=Long-Term",
            "": "https://etfdb.com/screener/#page={page}&"
            }
    # "https://etfdb.com/screener/#page=1&sort_direction=desc&sort_by=price&tab=overview&asset_class=equity&sizes=Small-Cap"
    # "https://etfdb.com/screener/#page=1&sort_direction=desc&sort_by=price&asset_class=equity&sizes=Large-Cap&investment_strategies=Value"
    for sort_name, sort_condition in sort_conditions.items():
        for url_name, url in urls.items():
            # df = pd.DataFrame()
            # for page in range(1, 3):
            n_url = url + sort_condition
            # print(n_url)
            # n_url = n_url.format(page = 20)
            # print(n_url)
            result = creater.get_etf_db_data(n_url, top=40)
            #     df = pd.concat([df, result])
            file_name = f"{sort_name}_{url_name}.xlsx" if url_name != "" else f"{sort_name}.xlsx"
            result.to_excel(f"ETF_list/{file_name}", index=0)
    
            print(file_name)
    
    # url = "https://etfdb.com/screener/#page={}&sort_direction=desc&sort_by=price"
    # # # final = "LSLT"
    # df = creater.get_etf_db_data(url, top=80)

    # df.to_excel("price.xlsx", index=0)
    # # url = "https://etfdb.com/screener/#page={}&sort_by=expense_ratio&sort_direction=asc"
    

if __name__ == "__main__":
    main()
