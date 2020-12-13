import pandas as pd

# def get_each_month_df(df):
#     df.date


df = pd.read_csv("共同資料/SPY.csv")
# print(df.head())
# close = df.close
df = df.reindex(index=df.index[::-1])
df["ema1"] = df.close.ewm(span=12, adjust= False).mean()
df["ema2"] = df.close.ewm(span=26, adjust= False).mean()
df["diff"] = df.ema1 - df.ema2
print(df.tail(10))
