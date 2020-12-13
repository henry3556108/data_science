import pandas as pd
import numpy as np
import re
def filter(s):
    chinese = '[\u4e00-\u9fa5]+'
    x = re.findall(chinese, s)
    # r1 = '[a-zA-Z0-9’!"#$%&\'()*+,-./:;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
    # x = re.sub(r1, '', s)
    if len(x) == 0:
        return None
    else:
        # print(x)
        return x[0]
    # print()

if __name__ == "__main__":
    df = pd.read_csv("test_v2.csv")
    df.columns = ["num", "tag", "total"]
    df["tag"] = df["tag"].apply(lambda x : filter(x))
    df = df.dropna(subset = ["tag"])
    df.to_excel("test_v3.xlsx", index = 0)
    # print(df.head())

