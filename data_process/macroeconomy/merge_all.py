import pandas as pd
import os
import time
def merge_weekly_and_monthly(monthly, src = "data_need", dst = "data_need/merge"):
    files = os.listdir(src)
    for f in files:
        if f.startswith("Weekly"):
            weekly = pd.read_csv(os.path.join(src, f))
            weekly.DATE = pd.to_datetime(weekly.DATE, format="%Y-%m-%d")
            weekly["year_month"] = weekly["DATE"].apply(lambda x : str(x.year) + str(x.month))
            monthly = pd.read_csv(monthly)
            monthly.year_month = monthly.year_month.astype(str)
            weekly = pd.merge(weekly, monthly, how="outer", left_on="year_month", right_on="year_month")
            # weekly = weekly[~weekly["DATE_x"].duplicated()]
            for c in ["DATE_x", "DATE_y", "year_month"]:
                try:
                    weekly = weekly.drop([c], axis = 1)
                except:
                    print(f"{c} has droped")
            weekly["point_sum"] = weekly.sum(axis = 1)
            print("complete drop")
            weekly.to_csv(os.path.join(dst, "merged_" + f), index = 0)
            print(f"complete save file：{f} at：{dst} folder")
    input("press enter to continue...")



if __name__ == "__main__":
    path = os.path.join("data_need", "merge", "merged_monthly.csv")
    merge_weekly_and_monthly(path)