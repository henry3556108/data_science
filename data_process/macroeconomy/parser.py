import pandas as pd
import datetime as dt
import os


def filter(df, start, end):
    # df = pd.read_csv("Weekly_Ending_Friday.csv")
    df["DATE"] = pd.to_datetime(df["DATE"], format="%Y-%m-%d")
    df = df.set_index("DATE")
    start = df.index.searchsorted(start)
    end = df.index.searchsorted(end)
    # print(df.head())
    df = df.iloc[start:end]
    return df
    # df.to_csv("data_need/{}.csv".format(name))


def diff(df, replace = False):
    indexs = df.index
    columns = df.columns
    new_df = df if replace == False else pd.DataFrame()
    for c in columns:
        tmp = []
        for i, date in enumerate(indexs):
            if i == 0:
                tmp.append(0)
            else:
                try:
                    current_value = float(df[c].loc[date])
                    pre_value = float(df[c].loc[indexs[i - 1]])
                    tmp.append(current_value - pre_value)
                except:
                    tmp.append(0)
        tmp = pd.DataFrame(tmp, columns=[f"{c}_diff"])
        tmp.index = indexs
        new_df = pd.concat([new_df, tmp], axis=1)
    return new_df

def diff_parser(src_dir):

    files = os.listdir(src_dir)
    for f in files:
        if f.endswith("csv"):
            df = pd.read_csv(os.path.join(src_dir, f), index_col=0)
            replace = True if input("要不要保留原本資料：y/n") == "y" else False
            if replace == True:
                df = diff(df, replace = True)
                file_name = f.replace(".csv", "_diff_only.csv")
            else:
                df = diff(df)
                df.to_csv(os.path.join(src_dir, "diff", file_name))

def filter_parser():
    dst = "data_need"
    os.makedirs(dst, exist_ok=True)
    start = dt.datetime(1998, 1, 1)
    end = dt.datetime(2010, 1, 1)
    files = os.listdir()
    for f in files:
        if f.endswith(".csv"):
            df = pd.read_csv(f)
            # print(df.head())
            df = filter(df, start, end)
            df.to_csv(os.path.join(dst, f))


if __name__ == "__main__":
    filter_parser()
    # diff_parser("data_need/")