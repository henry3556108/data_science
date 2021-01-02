import pandas as pd
import numpy as np


class Stock():
    def __init__(self, stock: pd.DataFrame(), name = None):
        self.stock = pd.DataFrame()
        stock.columns = [col.lower() for col in stock.columns]
        
        if name == None:
            self.stock["date"] = stock.date
            self.stock["close"] = stock.close
            self.stock["open"] = stock.open
            self.stock["high"] = stock.high
            self.stock["low"] = stock.low
            self.stock = self.stock.sort_values(by="date")
        else:
            self.stock["date"] = stock.date
            self.stock["close"] = stock[name.lower()]
        self.stock["close"] = pd.to_numeric(self.stock["close"], errors='coerce', downcast='float')
        self.stock = self.stock[~self.stock["close"].isna()]
        self.stock = self.stock.reset_index(drop = True)
        

    def get_stock(self):
        return self.stock

    def get_MACD(self, ema1=12, ema2=26, n3=9):
        df = self.stock
        macd = pd.DataFrame()
        macd["date"] = df.date
        macd["ema1"] = df["close"].ewm(span=ema1).mean()
        macd["ema2"] = df["close"].ewm(span=ema2).mean()
        macd["diff"] = macd["ema1"] - macd["ema2"]
        macd["macd"] = macd["diff"].ewm(span=n3).mean()
        macd["bar"] = macd["diff"] - macd["macd"]
        return macd
    
    def get_MA(self, period):
        df = self.stock
        ma = pd.DataFrame()
        tmp = []
        
        for index in df.index:
            close_slice = []
            if index < period - 1: 
                tmp.append(0)
                continue
            close_slice = df.iloc[index - period + 1: index + 1]["close"]
            tmp.append(close_slice.mean())
        ma["date"] = df.date
        ma[f"MA-{period}"] = tmp
        return ma
            # print(index)
        # df["ema1"] = df["close"].ewm(span=ema1).mean()
    


    def get_RSI(self, n1: int) -> pd.DataFrame():
        diff = [0]
        df = self.stock
        # print(self.stock)
        for index in df.index:
            # print(index)
            if index == 0:
                continue
            else:
                # print(df["close"][index])
                diff.append(df["close"][index] - df["close"][index - 1])
        rsi = []
        for index in df.index:
            if index < n1:
                rsi.append(0)
                continue
            tmp_data = diff[index - n1 + 1: index]
            positive = []
            negative = []
            for num in tmp_data:
                positive.append(num) if num > 0 else negative.append(num)
            positive_mean = 0.001 if len(positive) == 0 else abs(
                np.array(positive).sum() / n1) + 0.001
            negative_mean = 0.001 if len(negative) == 0 else abs(
                np.array(negative).sum() / n1) + 0.001
            rs = positive_mean / negative_mean
            cur_rsi = rs / (1 + rs) * 100
            rsi.append(cur_rsi)
        rsi = pd.DataFrame(rsi, columns=["rsi"])
        rsi = pd.concat([rsi, df["date"]], axis = 1)
        return rsi


if __name__ == "__main__":
    # pass

    # df = pd.read_csv("Quarterly.csv")
    # print(df.head())
    df = pd.read_csv("data_need/SPY.csv")
    # print(df.info())
    # print(df["date"].values)
    # dates = df["date"].values
    # n_dates = []
    # for date in dates:
    #     n_dates.append(date.replace("-", ""))
    # df["date"] = n_dates
    # print(df)
    # df["op1en"] = df["open"].apply(lambda x : str(x) + "hey")
    # print(df)
    # df = Stock(df)
    # df = Stock(df, name = "GDPC1_GDPPOT")
    # print(df.get_stock().head())
    # print(df.get_MACD().head())
    # print(df.get_stock().head(10))
    # print(df.get_MA(10).head(10))
    # print(df.get_RSI(9).head(10))
