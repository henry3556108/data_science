import pandas as pd

def get_data(file_name):
    df = pd.read_csv(file_name, index_col=0)
    return df

def get_ma(df, n = 20):
    df = df.reset_index()
    all_ma = []
    while len(all_ma) < n:
        all_ma.append(0)
    for i in range(len(df)  - n):
        ma = df.iloc[i: i + n].Close.values.mean()
        all_ma.append(ma)
        # print(closes)
        # break
    df["ma"] = all_ma
    # print(len(df), len(all_ma))
    # print(df.head(25))
    return df
    # pass

def get_out_of_range_prob(df, k, from_weekday = 3):
    df = df[df["contract"] != 0]
    uni_contracts = df["contract"].unique()
    time_out_of_range = 0
    # total = 0
    for uni_contract in uni_contracts:
        tmp = df[df["contract"] == uni_contract]
        first_day_open = tmp[tmp["weekday"] == from_weekday].head(1)["Close"].values[0]
        last_day_close = tmp[tmp["weekday"] == from_weekday].tail(1)["Close"].values[0]
        if k < 0:
            # print(first_day_open + k > last_day_close , time_out_of_range, first_day_open, last_day_close, k)
            if  first_day_open + k > last_day_close:
                time_out_of_range += 1
        if k > 0:
            if  first_day_open + k < last_day_close:
                time_out_of_range += 1
    prob = time_out_of_range / len(uni_contracts) * 100
    return prob

def get_prob_where_close_fall_below_ma(df):
    df = df[df["contract"] != 0]
    uni_contracts = df["contract"].unique()
    count = 0
    total = 0
    for uni_contract in uni_contracts:
        tmp = df[df["contract"] == uni_contract]
        first_day = tmp.head(1)
        last_day = tmp.tail(1)
        end_close = last_day.Close.values[0]
        ma = first_day.ma.values[0]
        close = first_day.Close.values[0]
        print(end_close, close, ma, close > ma, close > ma and end_close < ma)
        if close > ma and ma != 0:
            if end_close < ma:
                count += 1
            total += 1
    print(count / total)

def get_prob_where_close_breakthrough_ma(df):
    df = df[df["contract"] != 0]
    uni_contracts = df["contract"].unique()
    count = 0
    total = 0
    for uni_contract in uni_contracts:
        tmp = df[df["contract"] == uni_contract]
        first_day = tmp.head(1)
        last_day = tmp.tail(1)
        end_close = last_day.Close.values[0]
        ma = first_day.ma.values[0]
        close = first_day.Close.values[0]
        if close < ma and ma != 0:
            if end_close > ma:
                print(end_close, close, ma, close < ma, close < ma and end_close > ma)
                count += 1
            total += 1
    print(count / total)
        # print(ma, close)

def main():
    file_name = "everyday_close.csv"
    # file_name = "test_v4.csv"
    df = get_data(file_name)
    # ,.
    print(df.head())
    df = get_ma(df)
    get_prob_where_close_breakthrough_ma(df)
    # df.to_csv("every_day_close_have_20ma.csv", index = 0)
    # weekday = 3
    # with open(f"out_of_range_from_weekday_{weekday + 1}_low.txt", "w") as f:
    #     for k in range(-50, -500, -50):
    #         prob = get_out_of_range_prob(df, k, from_weekday = weekday)
    #         f.write(f"out of range {k} point porb is {round(prob, 3)}\n")

    # with open(f"out_of_range_from_weekday_{weekday + 1}_higher.txt", "w") as f:
    #     for k in range(50, 500, 50):
    #         prob = get_out_of_range_prob(df, k, from_weekday= weekday)
    #         f.write(f"out of range {k} point porb is {round(prob, 3)}\n")


    # uni_dates = df.Date.unique()
    # everday_close = pd.DataFrame()
    # for uni_date in uni_dates:
    #     current_date_df = df[df["Date"] == uni_date]
    #     first_data = current_date_df.head(1)
    #     print(first_data)
    #     first_data = first_data[["Date", "Open", "Close", "contract", "weekday", "timeStamp", "week"]]
    #     last_data = current_date_df.tail(1)
    #     last_data = last_data[["Date", "Open", "Close", "contract", "weekday", "timeStamp", "week"]]
    #     data = first_data
    #     data["Close"].values[0] = last_data["Close"].values[0]
    #     # print(last_data["Close"], data)
    #     # break
    #     everday_close = pd.concat([everday_close, data], axis = 0)
    # everday_close.to_csv("everyday_close.csv", index = 0)

    # pass


if __name__ == "__main__":
    main()