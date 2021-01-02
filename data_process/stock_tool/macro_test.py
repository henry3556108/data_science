from macro_point import MacroPointGetter
import pandas as pd
from stock import Stock
import numpy as np
from datetime import datetime


def test_monthly_point_data():
    monthly = pd.read_csv("data_need/Monthly.csv")
    getter = MacroPointGetter(monthly)
    points = getter.get_point()
    print(monthly.head())
    print(points.head())


def test_monthly_slice_time_data():
    df = pd.read_csv("data_need/merge/merged_Weekly_衰退.csv")
    slice_time = MacroPointGetter.get_slice_time(df, 160)
    # print(df.head())
    print(slice_time)


def test_getter_plot_none_stock():

    df = pd.read_csv("data_need/merge/merged_Weekly_衰退.csv")
    df2 = pd.read_csv("data_need/merge/merged_Weekly.csv")
    MacroPointGetter.plot(MacroPointGetter, points=df,
                          threadhold=160, stay=["point_sum"])
    MacroPointGetter.plot(MacroPointGetter, points=df2,
                          threadhold=160, stay=["point_sum"])


def test_getter_plot_stock():

    df = pd.read_csv("data_need/merge/merged_Weekly_衰退.csv")
    df2 = pd.read_csv("data_need/merge/merged_Weekly.csv")
    spy = Stock(pd.read_csv("data_need/SPY.csv"))
    MacroPointGetter.plot(MacroPointGetter, points=df, threadhold=160, stay=[
                          "point_sum"], other_stock=spy.get_stock())
    # MacroPointGetter.plot(MacroPointGetter, points=df2, threadhold = 130, stay=["point_sum"], other_stock = spy.get_stock())


def test_state():
    df = pd.read_csv("data_need/merge/merged_Weekly_衰退.csv")
    df2 = pd.read_csv("data_need/merge/merged_Weekly.csv")
    slice_time1 = MacroPointGetter.get_slice_time(df.copy(), 160)
    slice_time1 = pd.DataFrame(slice_time1)
    slice_time1[1] = "sure too cold"
    # print(slice_time1)
    slice_time2 = MacroPointGetter.get_slice_time(df2.copy(), 130)
    # print(slice_time2)
    slice_time2 = pd.DataFrame(slice_time2)
    slice_time2[1] = "trying too hot"
    slice_time3 = MacroPointGetter.get_slice_time(df2.copy(), 160)
    slice_time3 = pd.DataFrame(slice_time3)
    slice_time3[1] = "sure too hot"
    slice_time4 = MacroPointGetter.get_slice_time(df.copy(), 100)
    slice_time4 = pd.DataFrame(slice_time4)
    slice_time4[1] = "trying too cold"
    # print(slice_time4)
    slice_time = pd.concat(
        [slice_time1, slice_time2, slice_time3, slice_time4])
    slice_time = slice_time.reset_index(drop=True)
    slice_time = slice_time.sort_values(by="start")
    slice_time = MacroPointGetter.get_state(slice_time)
    # print(slice_time)


if __name__ == "__main__":
    # pass
    # test_monthly_point_data()
    # test_monthly_slice_time_data()
    # test_getter_plot_none_stock()
    # test_getter_plot_stock()
    # test_slice_time()
    test_state()
