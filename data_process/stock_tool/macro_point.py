from stock import Stock
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import dates as mdate
from datetime import datetime
import numpy as np


class MacroPointGetter():
    def __init__(self, df: pd.DataFrame):
        self.marco_data = {}
        # 裡面裝了很多 Stock
        tmp = df.copy()
        for col in df:
            tmp = df.copy()
            self.marco_data[col] = Stock(tmp, col)
            if col.lower() == "date":
                self.marco_data[col] = df[col]

    def point_center(self, name):
        # 以下是針對每一個不同資料的規則
        points = []
        if name == "RRSFS_PC1":
            rsi = self.marco_data[name].get_RSI(6)
            for v in rsi["rsi"].values:
                if v < 40:
                    points.append(15)
                else:
                    points.append(0)
        if name == "CSCICP03USM665S":
            macd = self.marco_data["CSCICP03USM665S"].get_MACD(3, 6, 5)
            diff = macd["diff"] < 0
            for v in diff.values:
                if v:
                    points.append(15)
                else:
                    points.append(0)

        if name == "GDPC1_GDPPOT":
            macd = self.marco_data[name].get_MACD(2, 8, 5)
            points = []
            point = 50
            p = 0
            for value in macd["diff"].values:
                p = point if value < 0 else 0
                points.append(p)

        if name == "GDPC1_PC1_GDP_PC1":
            macd = self.marco_data[name].get_MACD(2, 8, 5)
            points = [0]
            point = 50
            p = 0
            for index, value in enumerate(macd["diff"].values):
                if index == 0:
                    continue
                p = point if value < macd["diff"].values[index - 1] else 0
                points.append(p)
        if name.startswith("D"):
            point = 15
            points = [0]
            p = 0

            series = self.marco_data[name].get_stock().close
            for index, value in enumerate(series.values):
                if index == 0:
                    continue
                p = point if value > series[index - 1] else 0
                points.append(p)

        if name == "ICSA":
            rsi = self.marco_data[name].get_RSI(12)
            points = [0]
            point = 20
            p = 0
            for index, v in enumerate(rsi["rsi"].values):
                if index == 0:
                    continue

                p = point if v > 60 else p
                p = 0 if v < 40 else p
                points.append(p)

        if name == "STLFSI2_PC1":
            points = [0]
            point = 15
            p = 0
            series = self.marco_data[name].get_stock().close
            for index, v in enumerate(series.values):
                if index == 0:
                    continue
                p = 0 if series[index - 1] > 0 and v < 0 else p
                p = point if series[index - 1] < 0 and v > 0 else p
                points.append(p)

        points_df = pd.DataFrame(points, columns=[f"{name}_point"])
        return points_df

    def get_point(self):
        # 回傳一份全部都是分數外加日期的資料
        points = pd.DataFrame()
        for col in self.marco_data:
            if col.lower() == "date":
                continue
            points = pd.concat([self.point_center(col), points], axis=1)
        points = pd.concat([self.marco_data["DATE"], points], axis=1)
        return points

    def get_slice_time(points, threadhood):
        slice_time = []
        points["over_threadhood"] = points["point_sum"] > threadhood
        points = points[["DATE", "point_sum", "over_threadhood"]]
        start = end = None
        for index, value in enumerate(points["over_threadhood"].values):
            if value == True and start == None:
                start = index
            if value == True and start != None:
                end = index
            if value == False and start != None and index != len(points.index) - 1:
                slice_time.append(
                    [points.DATE.iloc[start], points.DATE.iloc[end + 1]])
                start = end = None
            elif index == len(points.index) - 1 and start != None:
                slice_time.append(
                    [points.DATE.iloc[start], points.DATE.iloc[end]])
        slice_time = pd.DataFrame(slice_time, columns=["start", "end"])
        return slice_time

    def plot(self, points, threadhold, hinds=[], stay=[], other_stock=pd.DataFrame()):
        ''' 不要塞超過太多的資料會很可怕\n
        hinds 裡面放陣列，看你不要哪一欄就放在裡面 像是這樣 ["某a欄", "某b欄"]\n
        stay 裡面也釋放陣列，有時候欄位太多不好刪，那就用這個吧\n
        other_stock 可以放一下你想觀測的股票，像是 SPY(不過記得篩選過，過濾時間區間)
        '''
        time_slices = None
        if "point_sum" in points.columns:
            time_slices = self.get_slice_time(points, threadhold)
        date = points["DATE"]
        if len(stay) != 0:
            points = points[stay]

        for hind in hinds:
            points = points.drop([hind], axis=1)
        fig, (axs) = plt.subplots(len(points.columns)
                                  ) if other_stock.empty else plt.subplots(len(points.columns) + 1)
        if other_stock.empty and len(stay) == 1:
            axs = [axs]
        for index, col in enumerate(points):
            y = points[col].values
            x = [datetime.strptime(str(d), '%Y-%m-%d').date() for d in date]
            alldays = mdate.YearLocator(1)  # 主刻度為每月
            axs[index].plot(x, y)
            plt.gcf().autofmt_xdate()
            axs[index].xaxis.set_major_formatter(
                mdate.DateFormatter('%Y-%m-%d'))
            axs[index].xaxis.set_major_locator(alldays)
            seasonLoc = mdate.MonthLocator(interval=3)  # 為 6 個月為 1 副刻度
            axs[index].xaxis.set_minor_locator(seasonLoc)
            axs[index].xaxis.set_minor_formatter(mdate.DateFormatter('%m'))
            axs[index].set_title(f"{col}")

            time_slices.apply(lambda x: axs[index].axvspan(x["start"],
                                                           x["end"], facecolor='green', alpha=0.5), axis=1)
            axs[index].tick_params(pad=10)

        if not other_stock.empty:

            x = [datetime.strptime(str(d), '%Y-%m-%d').date()
                 for d in other_stock.date]
            other_stock["date"] = other_stock["date"].apply(
                lambda x: pd.to_datetime(x, format='%Y-%m-%d'))
            for index, row in time_slices.iterrows():
                start = datetime.strptime(row["start"], "%Y-%m-%d")
                end = datetime.strptime(row["end"], "%Y-%m-%d")
                mask = (other_stock['date'] > start) & (
                    other_stock['date'] <= end)
                tmp = other_stock.loc[mask]
                start = tmp["date"].values[0]
                end = tmp["date"].values[-1]
                axs[-1].axvspan(start, end,
                                facecolor='red', alpha=0.5)
            axs[-1].set_title("stock")
            axs[-1].plot(x, other_stock.close)

        fig.tight_layout()
        plt.show()

    def get_state(df):
        dic = {"trying too hot": 3, "trying too cold": 1,
               "sure too hot": 0, "sure too cold": 2}
        re_dic = {value: key for (key, value) in dic.items()}
        df[1] = df[1].apply(lambda x : dic[x])
        df = df.reset_index(drop = True)
        states = []
        state = 2
        start_time = datetime.strptime("1900-1-1", "%Y-%m-%d")
        end_time = datetime.strptime("1900-1-1", "%Y-%m-%d")
        
        fig, ax = plt.subplots(1)
        for index, row in  df.iterrows():
            if state == 2 and row[1] == 2:
                start_time = datetime.strptime(row["start"], "%Y-%m-%d")
                end_time = datetime.strptime(row["end"], "%Y-%m-%d")
            if state == 2 and row[1] == 3:
                between_date = start_time <= datetime.strptime(row["start"], "%Y-%m-%d") <= end_time
                if between_date == False:
                    state = 3
            if state == 3 and row[1] == 0:
                state = 0
            if state == 0 and row[1] == 0:
                start_time = datetime.strptime(row["start"], "%Y-%m-%d")
                end_time = datetime.strptime(row["end"], "%Y-%m-%d")
            if state == 0 and row[1] == 1:
                between_date = start_time < datetime.strptime(row["start"], "%Y-%m-%d") < end_time
                if between_date != True:
                    state = 1
            if state == 1 and row[1] == 2:
                state = 2
            
            states.append(state)
        df["state"] = states
        spy = Stock(pd.read_csv("data_need/SPY.csv"))
        x = [datetime.strptime(str(d), '%Y-%m-%d').date()
                for d in spy.get_stock().date]
        for index in df.index:
            state = df["state"].iloc[index]
            start = datetime.strptime(df["start"].iloc[index], "%Y-%m-%d")
            end = datetime.strptime(df["start"].iloc[index + 1], "%Y-%m-%d") if index < df.index[-1] else datetime.strptime(df["end"].iloc[index], "%Y-%m-%d")
            color = None
            if state == 0:
                color = "green"
            if state == 1:
                color = "yellow"
            if state == 2:
                color = "blue"
            if state == 3:
                color = "red"
            ax.axvspan(start, end,
                            facecolor=color, alpha=0.5)
        
        # 如果要分開看在反註解下面的東西
        # for index, row in  df.iterrows():
        #     if row[1] == 0:
        #             start = datetime.strptime(row["start"], "%Y-%m-%d")
        #             end = datetime.strptime(row["end"], "%Y-%m-%d")
        #             ax[0].axvspan(start, end,
        #                             facecolor='red', alpha=0.5)
        #     if row[1] == 1:
        #             start = datetime.strptime(row["start"], "%Y-%m-%d")
        #             end = datetime.strptime(row["end"], "%Y-%m-%d")
        #             ax[1].axvspan(start, end,
        #                             facecolor='green', alpha=0.5)
        #     if row[1] == 2:
        #             start = datetime.strptime(row["start"], "%Y-%m-%d")
        #             end = datetime.strptime(row["end"], "%Y-%m-%d")
        #             ax[2].axvspan(start, end,
        #                             facecolor='yellow', alpha=0.5)
        #     if row[1] == 3:
        #             start = datetime.strptime(row["start"], "%Y-%m-%d")
        #             end = datetime.strptime(row["end"], "%Y-%m-%d")
        #             ax[3].axvspan(start, end,
        #                             facecolor='blue', alpha=0.5)
                
        ax.plot(x, spy.get_stock().close)
        # ax[0].plot(x, spy.get_stock().close)
        # ax[0].set_title(f"sure too hot")
        # ax[1].plot(x, spy.get_stock().close)
        # ax[1].set_title(f"try too cold")
        # ax[2].plot(x, spy.get_stock().close)
        # ax[2].set_title(f"sure too cold")
        # ax[3].plot(x, spy.get_stock().close)
        # ax[3].set_title(f"try too hot")
        
        fig.tight_layout()
        plt.show()
        return df




if __name__ == "__main__":
    pass
