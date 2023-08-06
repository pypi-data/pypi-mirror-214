import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import torch


class PreproccesorTimedelta:
    def __init__(self, items_length):
        self._length = items_length

    def initialize(self, data: pd.DataFrame):
        need_columns = ['event_id', '@timestamp']
        train = data[need_columns]
        train = train.rename(columns={'event_id': 'event', '@timestamp': 'timestamp'})
        train['timestamp'] = train['timestamp'].apply(
            lambda x: pd.Timestamp(pd.Timestamp(x).strftime('%Y-%m-%d %H:%M:%S')).timestamp())
        train.sort_values(by='timestamp', inplace=True, ignore_index=True)

        self.get_timediff(train)
        return train

    def sequence(self, data: pd.DataFrame):
        train = self.initialize(data)
        timedelta = train.timediff.values
        X, y = self.get_timediff_sequence(timedelta, self._length)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, shuffle=False)
        X_train = torch.Tensor(X_train)
        X_test = torch.Tensor(X_test)
        y_train = torch.Tensor(y_train)
        y_test = torch.Tensor(y_test)

        if torch.cuda.is_available():
            X_train = X_train.to("cuda")
            y_train = y_train.to("cuda")
            X_test = X_test.to("cuda")
            y_test = y_test.to("cuda")
        y_train = y_train.reshape(y_train.shape[0], 1)
        y_test = y_test.reshape(y_test.shape[0], 1)
        return X_train, X_test, y_train, y_test

    @staticmethod
    def get_timediff_sequence(values, k=1):
        X = []
        y = []
        for i in range(len(values) - k):
            temp_X = values[i:i + k]
            temp_y = np.array(values[i + k])
            X.append(temp_X)
            y.append(temp_y)
        X = np.array(X)
        y = np.array(y)
        to_array = lambda t: np.array(t)
        vfunc = np.vectorize(to_array)
        y = vfunc(y)
        return X, y

    @staticmethod
    def get_timediff(df):
        timediff = [0]
        timestamp = df['timestamp'].values
        for i in range(1, len(timestamp)):
            temp_timediff = abs(timestamp[i] - timestamp[i - 1])
            timediff.append(temp_timediff)
        df['timediff'] = timediff
