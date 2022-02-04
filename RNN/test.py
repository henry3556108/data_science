from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout, BatchNormalization
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def get_data():
    df = pd.read_csv("eth.csv")
    df.columns = ["date", "close", "open", "high", "low", "volume", "pct"]
    df.date = df.date.str.replace("年", "/")
    df.date = df.date.str.replace("月", "/")
    df.date = df.date.str.replace("日", "")
    df.date = pd.to_datetime(df.date)
    for col in df.columns[1:]:
        df[col] = df[col].str.replace(",", "")
        df[col] = df[col].str.replace("%", "")
        df[col] = df[col].str.replace("K", "")
        df[col] = df[col].str.replace("M", "")
        df[col] = df[col].str.replace("-", "")
        df[col] = pd.to_numeric(df[col], errors = "raise")
    return df

def get_train_data(eth, ratio = 0.3, length = 5):
    tmp = eth.copy(deep=True)
    recover = {"close":{}, "open": {}, "high": {}, "low": {}}
    recover["close"]["std"] = eth.close.std()
    recover["close"]["mean"] = eth.close.mean()
    recover["open"]["std"] = eth.open.std()
    recover["open"]["mean"] = eth.open.mean()   
    recover["high"]["std"] = eth.high.std()
    recover["high"]["mean"] = eth.high.mean()   
    recover["low"]["std"] = eth.low.std()
    recover["low"]["mean"] = eth.low.mean()   
    tmp.close = (eth.close - recover["close"]["mean"]) / recover["close"]["std"]
    tmp.open = (eth.open - recover["open"]["mean"]) / recover["open"]["std"]
    tmp.high = (eth.high - recover["high"]["mean"]) / recover["high"]["std"]
    tmp.low = (eth.low - recover["low"]["mean"]) / recover["low"]["std"]
    y = tmp.close[: -length]
    x = np.stack([tmp.loc[index + 1: index + length, "close":"low"] for index in y.index])
    x = np.reshape(x, (x.shape[0], x.shape[2], x.shape[1]))
    # x = np.reshape(x, (x.shape[0], x.shape[1]))
    index = list(tmp.index).index(int(len(tmp.index) * ratio))
    # index2 = list(tmp.index).index(int(len(tmp.index) * 0.8))
    x_train, x_test, y_train, y_test = x[index:], x[:], y[index:], y[:]
    # x_train = np.reshape(x_train, (1, x_train.shape[0], x_train.shape[1]))
    # x_test = np.reshape(x_test, (1, x_test.shape[0], x_test.shape[1]))
    return x_train, x_test, y_train, y_test, recover

def get_model(train_x):
    model = Sequential()
    print(train_x.shape)
    model.add(LSTM(units = 50, input_shape = (train_x.shape[1], train_x.shape[2])))
    model.add(BatchNormalization(momentum=0.98))
    model.add(Dense(units = 10))
    model.compile(optimizer = 'adam', loss = 'mean_squared_error')
    model.summary()
    return model

def recover_value(y, recover, col):
    return y * recover[col]["std"] + recover[col]["mean"]


if __name__ == "__main__":
    eth = get_data()
    train_x, test_x, train_y, test_y, recover = get_train_data(eth)
    # print(test_x[0], test_y.values[0], eth.head())
    model = get_model(train_x)
    model.fit(
        train_x, train_y,
        epochs=200, batch_size=16)
    predicted = model.predict(test_x)
    # print(predicted[:5], train_y.values[:5])
    predicted = np.reshape(predicted, (predicted.size,))
    test_y = recover_value(test_y, recover, "close")
    predicted = recover_value(predicted, recover, "close")
    predicted = np.reshape(predicted, (predicted.size,))
    print(predicted[:10], test_y[:10])
    plt.plot(test_y.values, color="b")
    plt.plot(predicted, color="r")
    plt.show()