import talib
import pandas as pd
from src.connectors.pg_conn import PgConnector #Для подключения к БД
from settings import * # Здесь хранятся данные для подключения к БД

def get_data():
    # Подсоединяемся к БД
    postgres = PgConnector(PG_DATABASE, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT)

    try:
        # Забираем данные из базы

        select = """WITH ranked_data AS (
                    SELECT
                        date,
                        tic,
                        open,
                        high,
                        low,
                        close,
                        volume,
                        ROW_NUMBER() OVER (PARTITION BY tic ORDER BY date DESC) AS rn
                    FROM t_real_data.trading_data)
                    SELECT
                        date,
                        tic,
                        open,
                        high,
                        low,
                        close,
                        volume
                    FROM ranked_data
                    WHERE rn <= 230
                    ORDER BY tic, date DESC;"""

        df = pd.DataFrame(
            postgres.get_data(select))

    finally:
        postgres.disconnect()

    rename_cols = {col: col.capitalize() for col in df.columns if col != 'tic'}
    df.rename(columns=rename_cols, inplace=True)

    return df

def feature(data):

    df = pd.DataFrame()
    for i in data["tic"].unique():
        data_temp = data.loc[data['tic'] == i].copy()
        data_temp.loc[:, ['sma_5']] = talib.SMA(data_temp["Close"], timeperiod=5)
        data_temp.loc[:, ['sma_10']] = talib.SMA(data_temp["Close"], timeperiod=10)
        data_temp.loc[:, ['sma_15']] = talib.SMA(data_temp["Close"], timeperiod=15)
        data_temp.loc[:, ['sma_20']] = talib.SMA(data_temp["Close"], timeperiod=20)
        data_temp.loc[:, ['sma_50']] = talib.SMA(data_temp["Close"], timeperiod=50)
        data_temp.loc[:, ['sma_200']] = talib.SMA(data_temp["Close"], timeperiod=200)
        data_temp.loc[:, ['sma_ratio_5_15']] = data_temp['sma_15'] / data_temp['sma_5']
        data_temp.loc[:, ['sma_ratio_10_50']] = data_temp['sma_50'] / data_temp['sma_15']
        data_temp.loc[:, ['sma_5_volume']] = talib.SMA(data_temp["Volume"], timeperiod=5)
        data_temp.loc[:, ['sma_10_volume']] = talib.SMA(data_temp["Volume"], timeperiod=10)
        data_temp.loc[:, ['sma_15_volume']] = talib.SMA(data_temp["Volume"], timeperiod=15)
        data_temp.loc[:, ['sma_50_volume']] = talib.SMA(data_temp["Volume"], timeperiod=50)
        data_temp.loc[:, ["sma_volume_ratio_5_15"]] = data_temp['sma_5_volume'] / data_temp['sma_15_volume']
        data_temp.loc[:, ["sma_volume_ratio_10_50"]] = data_temp['sma_10_volume'] / data_temp['sma_50_volume']
        data_temp.loc[:, ["ema_5"]] = talib.EMA(data_temp["Close"], timeperiod=5)
        data_temp.loc[:, ["ema_10"]] = talib.EMA(data_temp["Close"], timeperiod=10)
        data_temp.loc[:, ["ema_20"]] = talib.EMA(data_temp["Close"], timeperiod=20)
        data_temp.loc[:, ["ema_50"]] = talib.EMA(data_temp["Close"], timeperiod=50)
        data_temp.loc[:, ["ema_200"]] = talib.EMA(data_temp["Close"], timeperiod=200)

        # Calculate the Bollinger Bands
        data_temp.loc[:, ["upper_band"]], data_temp.loc[:, ["middle_band"]], data_temp.loc[:,
                                                                             ["lower_band"]] = talib.BBANDS(
            data_temp["Close"], timeperiod=20)

        # Calculate the relative strength index (RSI)
        data_temp.loc[:, ["rsi"]] = talib.RSI(data_temp["Close"], timeperiod=14)

        # Calculate the MACD
        data_temp.loc[:, ["macd"]], data_temp.loc[:, ["macd_signal"]], data_temp.loc[:, ["macd_hist"]] = talib.MACD(
            data_temp["Close"], 12, 26, 9)
        data_temp.loc[:, ['day_of_week']] = data_temp['Date'].dt.dayofweek
        data_temp.loc[:, ['lag_1day']] = data_temp['Close'].shift(1)
        data_temp.loc[:, ['adx_5']] = talib.ADX(data_temp['High'], data_temp['Low'], data_temp['Close'], timeperiod=5)
        data_temp.loc[:, ['adx_15']] = talib.ADX(data_temp['High'], data_temp['Low'], data_temp['Close'], timeperiod=15)

        data_temp.loc[:, ['rsi_5']] = talib.RSI(data_temp['Close'], timeperiod=5)
        data_temp.loc[:, ['rsi_15']] = talib.RSI(data_temp['Close'], timeperiod=15)
        data_temp.loc[:, ['rsi_ratio']] = data_temp['rsi_5'] / data_temp['rsi_15']

        data_temp.loc[:, ['roc']] = talib.ROC(data_temp['Close'], timeperiod=15)

        data_temp.loc[:, ['hammer']] = talib.CDLHAMMER(data_temp['Open'], data_temp['High'], data_temp['Low'],
                                                       data_temp['Close'])
        data_temp.loc[:, ['shooting_star']] = talib.CDLSHOOTINGSTAR(data_temp['Open'], data_temp['High'],
                                                                    data_temp['Low'], data_temp['Close'])
        data_temp.loc[:, ['engulfing']] = talib.CDLENGULFING(data_temp['Open'], data_temp['High'], data_temp['Low'],
                                                             data_temp['Close'])
        data_temp.loc[:, ['morning_star']] = talib.CDLMORNINGSTAR(data_temp['Open'], data_temp['High'],
                                                                  data_temp['Low'], data_temp['Close'])
        data_temp.loc[:, ['evening_star']] = talib.CDLEVENINGSTAR(data_temp['Open'], data_temp['High'],
                                                                  data_temp['Low'], data_temp['Close'])
        data_temp.loc[:, ['marubozu']] = talib.CDLMARUBOZU(data_temp['Open'], data_temp['High'], data_temp['Low'],
                                                           data_temp['Close'])
        data_temp.loc[:, ['doji']] = talib.CDLDOJI(data_temp['Open'], data_temp['High'], data_temp['Low'],
                                                   data_temp['Close'])
        data_temp.dropna(inplace=True)
        df = pd.concat([df, data_temp], ignore_index=True)
    return df

def format_data(df, features):
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    df[features] = df[features].astype(float)
    # Формируем нужную структуру
    result = {
        "data": [
            {
                "ticker": ticker,
                "vectors": group[['Date']].apply(
                    lambda row: {
                        "date": row['Date'],
                        "vector": group.loc[row.name, features].tolist()
                    },
                    axis=1
                ).tolist()
            }
            for ticker, group in df.groupby('tic')
        ]
    }
    return result

if __name__ == "__main__":

    df = get_data()
    df = feature(df)
    print (df['tic'].value_counts())

    features = ['Close', 'sma_5', 'sma_10', 'sma_15', 'sma_50', 'sma_200', 'sma_ratio_5_15', 'sma_ratio_10_50',
            'sma_5_volume', 'sma_10_volume', 'sma_15_volume', 'sma_50_volume', 'sma_volume_ratio_5_15',
            'sma_volume_ratio_10_50', 'upper_band',
            'middle_band', 'lower_band', 'rsi', 'macd', 'macd_signal', 'macd_hist','day_of_week','lag_1day',#'cA5', 'cD5', 'cD4', 'cD3', 'cD2', 'cD1',#'wavelet_forecast',
            'adx_5', 'adx_15', 'rsi_5', 'rsi_15', 'rsi_ratio', 'roc','hammer','shooting_star','engulfing',
            'morning_star','evening_star','marubozu','doji']

    result = format_data(df, features)

    import json
    with open(r'C:\Users\zarocool\Documents\Обучение_ML\Homework\8HW\output.json', "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4, ensure_ascii=False)