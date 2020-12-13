import pandas as pd
import os

def merge_season(src = "data_need", dst = "data_need/merge"):
    os.makedirs(src, exist_ok=True)
    os.makedirs(dst, exist_ok=True)
    files = os.listdir(src)
    dfs_done = []
    for i in range(0, 3):
        df_names = []
        dfs = []
        df = pd.DataFrame()
        for f in files:
            if f.startswith("Quarterly"):
                df_names.append(f)
        for f in df_names:
            dfs.append(pd.read_csv(os.path.join(src, f)))
        for index in range(len(dfs)):
            if df.empty:
                df = dfs[index]
            else:
                df = pd.merge(df, dfs[index],left_on="DATE", right_on="DATE")
        df.DATE = pd.to_datetime(df.DATE, format = "%Y-%m-%d")
        df["year_month"] = df["DATE"].apply(lambda x : str(x.year) + str(x.month+i))
        dfs_done.append(df)
    df = pd.concat(dfs_done, axis=0)
    df = df.sort_values(by="DATE")
    df.to_csv(os.path.join(dst, "Quarterly.csv"), index = 0)

def merge_each_month(src = "data_need", dst = "data_need/merge/"):

    files = os.listdir(src)
    dfs = []
    for f in files:
        if f.startswith("Month") and f.endswith(".csv"):
            tmp = pd.read_csv(os.path.join(src, f))
            tmp.DATE = pd.to_datetime(tmp.DATE, format = "%Y-%m-%d")
            tmp["year_month"] = tmp["DATE"].apply(lambda x : str(x.year) + str(x.month))
            dfs.append(tmp)
    df = pd.concat(dfs)
    df.to_csv(os.path.join(dst, "Monthly.csv"), index = 0)

def merge_quarterly_monthly(src = "data_need/merge"):
    files = os.listdir(src)
    dfs = []
    df = pd.DataFrame()
    for f in files:
        # print(f)
        if f.endswith(".csv") and not f.startswith("merged"):
            tmp = pd.read_csv(os.path.join(src, f))
            tmp["year_month"] = tmp["year_month"].astype("str")
            # print(tmp.head())
            dfs.append(tmp)
    print(len(dfs))
    for index in range(len(dfs)):
        if df.empty:
            df = dfs[index]
        else:
            df = pd.merge(df, dfs[index],left_on="year_month", right_on="year_month")
    df = df.drop(["DATE_y"], axis = 1)
    df.to_csv(os.path.join(src, "merged_monthly.csv"), index=0)

if __name__ == "__main__":
    merge_season()
    merge_each_month()
    merge_quarterly_monthly()