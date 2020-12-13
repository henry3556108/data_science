import merge_quarterly_monthly, merge_all
import os
if __name__ == "__main__":
    merge_quarterly_monthly.merge_season(src = "data_need/point", dst="data_need/merge")
    merge_quarterly_monthly.merge_each_month(src = "data_need/point", dst="data_need/merge")
    merge_quarterly_monthly.merge_quarterly_monthly(src = "data_need/merge")
    merge_all.merge_weekly_and_monthly(os.path.join("data_need", "merge", "merged_monthly.csv"), src = "data_need/point")