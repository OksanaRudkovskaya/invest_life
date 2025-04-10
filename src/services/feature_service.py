import talib
import pandas as pd

def feature(data):
    df = pd.DataFrame()
    for i in data["tic"].unique():
        data_temp = data.loc[data['tic'] == i].copy()
        data_temp.loc[:, ['sma_5']] = talib.SMA(data_temp["close"], timeperiod=5)
        data_temp.loc[:, ['sma_10']] = talib.SMA(data_temp["close"], timeperiod=10)
        data_temp.loc[:, ['sma_15']] = talib.SMA(data_temp["close"], timeperiod=15)
        data_temp.loc[:, ['sma_20']] = talib.SMA(data_temp["close"], timeperiod=20)
        data_temp.loc[:, ['sma_50']] = talib.SMA(data_temp["close"], timeperiod=50)
        data_temp.loc[:, ['sma_200']] = talib.SMA(data_temp["close"], timeperiod=200)
        data_temp.loc[:, ['sma_ratio_5_15']] = data_temp['sma_15'] / data_temp['sma_5']
        data_temp.loc[:, ['sma_ratio_10_50']] = data_temp['sma_50'] / data_temp['sma_15']
        data_temp.loc[:, ['sma_5_volume']] = talib.SMA(data_temp["volume"], timeperiod=5)
        data_temp.loc[:, ['sma_10_volume']] = talib.SMA(data_temp["volume"], timeperiod=10)
        data_temp.loc[:, ['sma_15_volume']] = talib.SMA(data_temp["volume"], timeperiod=15)
        data_temp.loc[:, ['sma_50_volume']] = talib.SMA(data_temp["volume"], timeperiod=50)
        data_temp.loc[:, ["sma_volume_ratio_5_15"]] = data_temp['sma_5_volume'] / data_temp['sma_15_volume']
        data_temp.loc[:, ["sma_volume_ratio_10_50"]] = data_temp['sma_10_volume'] / data_temp['sma_50_volume']
        data_temp.loc[:, ["ema_5"]] = talib.EMA(data_temp["close"], timeperiod=5)
        data_temp.loc[:, ["ema_10"]] = talib.EMA(data_temp["close"], timeperiod=10)
        data_temp.loc[:, ["ema_20"]] = talib.EMA(data_temp["close"], timeperiod=20)
        data_temp.loc[:, ["ema_50"]] = talib.EMA(data_temp["close"], timeperiod=50)
        data_temp.loc[:, ["ema_200"]] = talib.EMA(data_temp["close"], timeperiod=200)

        # Calculate the Bollinger Bands
        data_temp.loc[:, ["upper_band"]], data_temp.loc[:, ["middle_band"]], data_temp.loc[:,
                                                                             ["lower_band"]] = talib.BBANDS(
            data_temp["close"], timeperiod=20)

        # Calculate the relative strength index (RSI)
        data_temp.loc[:, ["rsi"]] = talib.RSI(data_temp["close"], timeperiod=14)

        # Calculate the MACD
        data_temp.loc[:, ["macd"]], data_temp.loc[:, ["macd_signal"]], data_temp.loc[:, ["macd_hist"]] = talib.MACD(
            data_temp["close"], fastperiod=12, slowperiod=26, signalperiod=9)

        data_temp.loc[:, ['adx_5']] = talib.ADX(data_temp['high'], data_temp['low'], data_temp['close'], timeperiod=5)
        data_temp.loc[:, ['adx_15']] = talib.ADX(data_temp['high'], data_temp['low'], data_temp['close'], timeperiod=15)

        data_temp.loc[:, ['rsi_5']] = talib.RSI(data_temp['close'], timeperiod=5)
        data_temp.loc[:, ['rsi_15']] = talib.RSI(data_temp['close'], timeperiod=15)
        data_temp.loc[:, ['rsi_ratio']] = data_temp['rsi_5'] / data_temp['rsi_15']

        data_temp.loc[:, ['roc']] = talib.ROC(data_temp['close'], timeperiod=15)

        data_temp.loc[:, ['hammer']] = talib.CDLHAMMER(data_temp['open'], data_temp['high'], data_temp['low'],
                                                       data_temp['close'])
        data_temp.loc[:, ['shooting_star']] = talib.CDLSHOOTINGSTAR(data_temp['open'], data_temp['high'],
                                                                    data_temp['low'], data_temp['close'])
        data_temp.loc[:, ['engulfing']] = talib.CDLENGULFING(data_temp['open'], data_temp['high'], data_temp['low'],
                                                             data_temp['close'])
        data_temp.loc[:, ['morning_star']] = talib.CDLMORNINGSTAR(data_temp['open'], data_temp['high'],
                                                                  data_temp['low'], data_temp['close'])
        data_temp.loc[:, ['evening_star']] = talib.CDLEVENINGSTAR(data_temp['open'], data_temp['high'],
                                                                  data_temp['low'], data_temp['close'])
        data_temp.loc[:, ['marubozu']] = talib.CDLMARUBOZU(data_temp['open'], data_temp['high'], data_temp['low'],
                                                           data_temp['close'])
        data_temp.loc[:, ['doji']] = talib.CDLDOJI(data_temp['open'], data_temp['high'], data_temp['low'],
                                                   data_temp['close'])
        data_temp.dropna(inplace=True)
        df = pd.concat([df, data_temp], ignore_index=True)
    return df

