import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import timedelta


def lr_prediction(stock):
    # Running ML
    df = pd.read_csv(stock)
    df['day'] = pd.to_datetime(df['day'])
    dataframe = df.head(100)
    df['lclose'] = df.close.shift(-1)
    df['2 days STD'] = df.lclose.rolling(window=2).std().shift(-1)
    df['2 days MA'] = df.lclose.rolling(window=2).mean().shift(-1)
    df['7 days STD'] = df.lclose.rolling(window=7).std().shift(-6)
    df['7 days MA'] = df.lclose.rolling(window=7).mean().shift(-6)
    df['14 days MA'] = df.lclose.rolling(window=14).mean().shift(-13)
    df['21 days MA'] = df.lclose.rolling(window=21).mean().shift(-20)
    df['lagged volume'] = df.volume.shift(-1)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(subset=['21 days MA'], inplace=True)
    X = df[
        ['lclose', 'lagged volume', '21 days MA', '14 days MA', '7 days MA', '7 days STD', '2 days MA', '2 days STD']]
    Y = df['close']
    lr_model = LinearRegression()
    lr_model.fit(X, Y)

    # Predicting
    df1 = pd.DataFrame([[np.nan] * len(dataframe.columns)], columns=dataframe.columns)
    df1['day'] = dataframe['day'].values[0]
    df1['day'] = df1['day'].astype(object)
    df1['day'] = df1['day'] + timedelta(days=1)
    dataframe = pd.concat([df1, dataframe]).reset_index(drop=True)
    dataframe['lclose'] = dataframe.close.shift(-1)
    dataframe['2 days STD'] = dataframe.lclose.rolling(window=2).std().shift(-1)
    dataframe['2 days MA'] = dataframe.lclose.rolling(window=2).mean().shift(-1)
    dataframe['7 days STD'] = dataframe.lclose.rolling(window=7).std().shift(-6)
    dataframe['7 days MA'] = dataframe.lclose.rolling(window=7).mean().shift(-6)
    dataframe['14 days MA'] = dataframe.lclose.rolling(window=14).mean().shift(-13)
    dataframe['21 days MA'] = dataframe.lclose.rolling(window=21).mean().shift(-20)
    dataframe['lagged volume'] = dataframe.volume.shift(-1)
    dataframe.replace([np.inf, -np.inf], np.nan, inplace=True)
    dataframe.dropna(subset=['21 days MA'], inplace=True)
    X_data = dataframe[
        ['lclose', 'lagged volume', '21 days MA', '14 days MA', '7 days MA', '7 days STD', '2 days MA', '2 days STD']]
    result = dataframe[['day', 'close']]
    result['pclose'] = lr_model.predict(X_data)
    result = result.fillna('null')
    result = result.reindex(index=result.index[::-1])

    return result
