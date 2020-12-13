import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np


def get_convert_point(series, point, below_zero=True):
    flag = 0
    values = []
    p = 0
    points = []
    for v in series.values:
        if len(values) == 0:
            values.append(v)
        if len(values) >= 1 and v != values[0]:
            values.insert(0, v)
            # print(values)
        if len(values) >= 3:
            if below_zero == True:
                if values[1] < 0 and values[0] - values[1] > 0 and values[1] - values[2] < 0:
                    p = point
            else:
                if values[0] - values[1] > 0 and values[1] - values[2] < 0:
                    p = point

            if p == point and values[0] < values[1] and values[1] > values[2]:
                p = 0
        points.append(p)

    points = pd.Series(points, name=series.name+"_convert_point")
    return points


def get_new_record_point(series, point: int, n1: int = 20) -> pd.DataFrame():
    points = []
    while len(points) < n1:
        points.append(0)

    for index in range(n1 - 1, len(series)):
        tmp_data = series[index - n1 + 1: index]
        cur_value = series[index]
        maximum = tmp_data.max()
        p = 0
        p = point if cur_value < maximum else p
        p = 0 if cur_value == maximum else p
        points.append(p)
    return pd.Series(points, name=f"{series.name}_new_record_point")


def get_rsi(series: pd.Series(), n1: int) -> pd.DataFrame():
    diff = [0]
    for index in series.index:
        if index == 0:
            continue
        else:
            diff.append(series[index] - series[index - 1])
    rsi = []

    for index in series.index:
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
        # print(len(positive), positive_mean, len(negative), negative_mean, rs)

        cur_rsi = rs / (1 + rs) * 100
        # print(cur_rsi)
        rsi.append(cur_rsi)
    return pd.DataFrame(rsi, columns=["rsi"])


def get_rsi_point(series: pd.Series(), point: int) -> pd.DataFrame():
    rsi = get_rsi(series, 6)
    # print(rsi.head(20))
    p = 0
    points = []
    for cur_rsi in rsi["rsi"].values:
        p = point if cur_rsi > 50 else p
        p = 0 if cur_rsi < 50 else p
        points.append(p)

    points = pd.Series(points, name=f"{series.name}_rsi_point")
    return points


def get_MACD(series: pd.Series(), n1: int = 12, n2: int = 26, n3: int = 9) -> pd.DataFrame():
    df = pd.DataFrame(series)

    name = series.name
    df["ema1"] = df[name].ewm(span=n1).mean()
    df["ema2"] = df[name].ewm(span=n2).mean()
    df["diff"] = df["ema1"] - df["ema2"]
    df["macd"] = df["diff"].ewm(span=n3).mean()
    df["bar"] = df["diff"] - df["macd"]
    ls = []
    bars = df.bar.values
    for i in range(len(df.bar.values)):
        if i < 2:
            ls.append(0)
            continue
        bar_diff = bars[i] - bars[i-1]
        ls.append(bar_diff)
    df["bar_diff"] = pd.Series(ls)
    return df


def get_macd_point(series: pd.Series(), point: int):
    macd = get_MACD(series, 3, 10, 5)
    points = []
    diff = macd["macd"].values
    p = 0
    for i in range(len(diff)):
        if i < 2:
            points.append(0)
            continue
        # p = point if diff[i] > 0
        p = point if macd["diff"][i - 1] > 0 and macd["diff"][i] < 0 else p
        p = 0 if macd["diff"][i - 1] < 0 and macd["diff"][i] > 0 else p
        # p = point if macd["diff"][i - 1] > macd["macd"][i -
        #                                                 1] and macd["diff"][i] < macd["macd"][i] else p
        # p = 0 if macd["diff"][i - 1] < macd["macd"][i -
        #                                             1] and macd["diff"][i] > macd["macd"][i] else p
        points.append(p)
    points = pd.Series(points, name=f"{series.name}_macd_point")
    return points


def main():
    Weekly_points_strategy = [
        ("CCSA", 30, get_macd_point), ("ICSA_CHG", 20, get_macd_point)]
    Monthly_points_strategy = [("DGORDER_PC1", 10, get_rsi_point), ("PCE_PC1", 10, get_rsi_point), ("RRSFS_PC1", 5, get_convert_point), (
        "PCEDG_PC1", 5, get_convert_point), ("UEMPLT5", 20, get_macd_point), ("UNRATE", 50, get_new_record_point)]
    Quarterly_points_strategy = [("EXPGSC1_PC1", 30, get_convert_point), (
        "IMPGSC1_PC1", 20, get_convert_point), ("PNFI_PC1", 20, get_convert_point)]

    file_name = "Monthly"
    points_strategy = Monthly_points_strategy

    # df = pd.read_excel(file_name + ".xlsx")
    df = pd.read_csv(file_name + ".csv")

    points = pd.DataFrame()
    for (col, point, strategy) in points_strategy:
        points = pd.concat([points, strategy(df[col], point)], axis=1)

    points = pd.concat([df["DATE"], points], axis=1)
    points.to_csv(os.path.join("point", file_name + ".csv"), index=False)


if __name__ == "__main__":
    main()
