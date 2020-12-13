import pandas as pd
import datetime


def concat_column(x):
    timestamp = x.Date + " " + x.Time
    # timestamp = pd.to_datetime(x)
    return timestamp
    # print(timestamp)
    # print(x)
    # assert False


def get_week_of_month(year, month, day):
    """
    獲取指定的某天是某個月中的第幾周
    週一作為一週的開始
    """
    end = int(datetime.datetime(year, month, day).strftime("%W"))
    begin = int(datetime.datetime(year, month, 1).strftime("%W"))
    return end - begin


def filter_every_contract(x):
    year = x.year
    month = x.month
    day = x.day
    weekday = x.weekday
    flag = 0
    week_of_month = get_week_of_month(year, month, day)
    if week_of_month < 2:
        flag = 0
    elif week_of_month == 2:
        if weekday < 3:
            flag = 0
        else:
            flag = 1
    else:
        flag = 1

    return month + flag - 1

def get_last_close(x):
    try:
        contract = x.contract
        
    except:
        pass

def get_data(file_name, processed = False):
    if processed == False:
        df = pd.read_csv(file_name)
        # print(df.head(), df.tail())
        df["timeStamp"] = df.apply(lambda x: concat_column(x), axis=1)
        df["timeStamp"] = pd.to_datetime(
            df["timeStamp"], format="%Y/%m/%d %H:%M:%S", errors='ignore')
        print("end timeStamp")
        df["weekday"] = df.timeStamp.dt.dayofweek
        df["month"] = df.timeStamp.dt.month
        df["year"] = df.timeStamp.dt.year
        df["day"] = df.timeStamp.dt.day
        df["contract"] = df.apply(lambda x: filter_every_contract(x), axis=1)
        print("end contract")
        uni_contracts = df.contract.unique()
        pervious_closes = {}
        for uni_contract in uni_contracts:
            tmp = df[df["contract"] == uni_contract]
            first_data = tmp.head(1)
            close = first_data.Open
            pervious_closes[uni_contract] = float(close.values)
        print("end find pervious close")
        df["pervious_close"] = df.apply(lambda x :
        pervious_closes[x.contract], axis = 1)
    else:
        df = pd.read_csv(file_name)    
    return df

def get_close_out_of_range_to_txt(df, bound):
    each_contract_datas = []
    uni_contracts = df.contract.unique()
    for uni_contract in uni_contracts:
        with open(f"out_of_range {bound}.txt", "a") as f:
            contract_data = df[df["contract"] == uni_contract]
            contract_data["is_out_of_range"] = contract_data.apply(lambda x : abs(x.Close - x.pervious_closes) > bound, axis = 1)
            len_of_contract = len(contract_data["is_out_of_range"])
            out_of_range = len(contract_data[contract_data["is_out_of_range"] == True])
            f.write(f"{str(uni_contract)}, {str(out_of_range / len_of_contract)} \n")
        
def get_close_out_of_range_to_csv(df, bound):
    df["is_out_of_range"] = df.apply(lambda x : abs(x.Close - x.pervious_closes) > bound, axis = 1)
    df.to_csv(f"get_out_of_range_{bound}.csv", index = False)

def get_day_close(df):
    uni_days = df.Date.unique()
    uni_days_close = pd.DataFrame()
    for uni_day in uni_days:
        tmp = df[df["Date"] == uni_day]
        uni_days_close = pd.concat([uni_days_close, tmp.tail(1)])
    uni_days_close.to_csv("every_day_close.csv", index=False)


def main():
    df = get_data("test_v4.csv", processed = True)

    # for bound in range(500, 1000, 100):
    #     get_close_out_of_range_to_txt(df, bound)
    #     get_close_out_of_range_to_csv(df, bound)
    get_day_close(df)



if __name__ == "__main__":
    main()
# df.set_index("timeStamp", inplace = True)
# print(df.between_time("2020", "2020"))
# print(df.info())

# df.Date = pd.to_datetime(df.Date, format='H%:M%')
