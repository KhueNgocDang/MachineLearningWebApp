import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from datetime import timedelta
from firstPage.models import *


def fetch_csv(symbol):
    return pd.DataFrame.from_records(
        StockInfo.objects.all().filter(ticker__ticker=symbol).values_list('day', 'close', 'volume'),
        columns=['day', 'close', 'volume']
    )


def lr_prediction(df):
    # Running ML
    df['day'] = pd.to_datetime(df['day'])
    df1 = pd.DataFrame([[np.nan] * len(df.columns)], columns=df.columns)
    df1['day'] = df['day'].values[0]
    df1['day'] = df1['day'].astype(object)
    df1['day'] = df1['day'] + timedelta(days=1)
    df = pd.concat([df1, df]).reset_index(drop=True)
    df['lclose'] = df.close.shift(-1)
    df['7 days STD'] = df.lclose.rolling(window=7).std().shift(-6)
    df['7 days MA'] = df.lclose.rolling(window=7).mean().shift(-6)
    df['14 days MA'] = df.lclose.rolling(window=14).mean().shift(-13)
    df['21 days MA'] = df.lclose.rolling(window=21).mean().shift(-20)
    df['lagged volume'] = df.volume.shift(-1)
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    dataframe = df.head(30)
    dataframe.dropna(subset=['21 days MA'], inplace=True)
    df.dropna(inplace=True)

    X = df[
        ['lclose', 'lagged volume', '21 days MA', '14 days MA', '7 days MA', '7 days STD']]
    Y = df['close']
    lr_model = LinearRegression()
    lr_model.fit(X, Y)

    # Predicting
    X_data = dataframe[
        ['lclose', 'lagged volume', '21 days MA', '14 days MA', '7 days MA', '7 days STD']]
    result = dataframe[['day', 'close']]
    result['pclose'] = lr_model.predict(X_data)
    result = result.fillna('null')
    result = result.reindex(index=result.index[::-1])

    # Convert result into json
    result['day'] = pd.to_datetime(result.day, format='%Y-%m-%d')
    result['day'] = result['day'].dt.strftime('%Y-%m-%d')
    data = result.set_index('day')
    out = {'labels': data.index.tolist(), 'datasets': []}
    out['datasets'].append({
        'label': 'Giá trị thật',
        'data': data['close'].values.tolist(),
        'backgroundColor': 'rgba(255,99,132,0.2)'
    })
    out['datasets'].append({
        'label': 'Giá trị dự đoán',
        'data': data['pclose'].values.tolist(),
        'backgroundColor': 'rgba(54,162,64,0.2)'
    })

    return out
