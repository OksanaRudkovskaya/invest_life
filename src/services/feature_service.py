import talib
import pandas as pd
import numpy as np

def feature(data):
    df = pd.DataFrame()
    for i in data["tic"].unique():
        data_temp = data.loc[data['tic'] == i]
        data_temp.loc[:, ['sma_5']] = talib.SMA(data_temp["Close"], timeperiod=5)
        data_temp.loc[:, ['sma_10']] = talib.SMA(data_temp["Close"], timeperiod=10)
        data_temp.loc[:, ['sma_15']] = talib.SMA(data_temp["Close"], timeperiod=15)
        data_temp.loc[:, ['sma_20']] = talib.SMA(data_temp["Close"], timeperiod=20)
        data_temp.loc[:, ['sma_50']] = talib.SMA(data_temp["Close"], timeperiod=50)
        data_temp.loc[:, ['sma_200']] = talib.SMA(data_temp["Close"], timeperiod=200)
        data_temp.loc[:, ['sma_ratio_5_15']] = data_temp['sma_15'] / data_temp['sma_5']
        data_temp.loc[:, ['sma_ratio_10_50']] = data_temp['sma_50'] / data_temp['sma_15']
        data_temp.loc[:, ['sma_5_Volume']] = talib.SMA(data_temp["Volume"], timeperiod=5)
        data_temp.loc[:, ['sma_10_Volume']] = talib.SMA(data_temp["Volume"], timeperiod=10)
        data_temp.loc[:, ['sma_15_Volume']] = talib.SMA(data_temp["Volume"], timeperiod=15)
        data_temp.loc[:, ['sma_50_Volume']] = talib.SMA(data_temp["Volume"], timeperiod=50)
        data_temp.loc[:, ["sma_Volume_ratio_5_15"]] = data_temp['sma_5_Volume'] / data_temp['sma_15_Volume']
        data_temp.loc[:, ["sma_Volume_ratio_10_50"]] = data_temp['sma_10_Volume'] / data_temp['sma_50_Volume']
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
        data_temp.loc[:, ["RSI"]] = talib.RSI(data_temp["Close"], timeperiod=14)

        # Calculate the MACD
        data_temp.loc[:, ["macd"]], data_temp.loc[:, ["macd_signal"]], data_temp.loc[:, ["macd_hist"]] = talib.MACD(
            data_temp["Close"], fastperiod=12, slowperiod=26, signalperiod=9)

        data_temp.loc[:, ['ADX_5']] = talib.ADX(data_temp['High'], data_temp['Low'], data_temp['Close'], timeperiod=5)
        data_temp.loc[:, ['ADX_15']] = talib.ADX(data_temp['High'], data_temp['Low'], data_temp['Close'], timeperiod=15)

        data_temp.loc[:, ['RSI_5']] = talib.RSI(data_temp['Close'], timeperiod=5)
        data_temp.loc[:, ['RSI_15']] = talib.RSI(data_temp['Close'], timeperiod=15)
        data_temp.loc[:, ['RSI_ratio']] = data_temp['RSI_5'] / data_temp['RSI_15']

        data_temp.loc[:, ['ROC']] = talib.ROC(data_temp['Close'], timeperiod=15)

        data_temp.loc[:, ['HAMMER']] = talib.CDLHAMMER(data_temp['Open'], data_temp['High'], data_temp['Low'],
                                                       data_temp['Close'])
        data_temp.loc[:, ['SHOOTING_STAR']] = talib.CDLSHOOTINGSTAR(data_temp['Open'], data_temp['High'],
                                                                    data_temp['Low'], data_temp['Close'])
        data_temp.loc[:, ['ENGULFING']] = talib.CDLENGULFING(data_temp['Open'], data_temp['High'], data_temp['Low'],
                                                             data_temp['Close'])
        data_temp.loc[:, ['MORNING_STAR']] = talib.CDLMORNINGSTAR(data_temp['Open'], data_temp['High'],
                                                                  data_temp['Low'], data_temp['Close'])
        data_temp.loc[:, ['EVENING_STAR']] = talib.CDLEVENINGSTAR(data_temp['Open'], data_temp['High'],
                                                                  data_temp['Low'], data_temp['Close'])
        data_temp.loc[:, ['MARUBOZU']] = talib.CDLMARUBOZU(data_temp['Open'], data_temp['High'], data_temp['Low'],
                                                           data_temp['Close'])
        data_temp.loc[:, ['DOJI']] = talib.CDLDOJI(data_temp['Open'], data_temp['High'], data_temp['Low'],
                                                   data_temp['Close'])
        # Определим, что значение таргета это рост завтрашней цены относительно текущей, с учетом комиссии в 1$
        data_temp.loc[:, ['target']] = np.where(-data_temp['Close'].diff(periods=-1) > 1, True, False)
        data_temp.loc[:, ['diff']] = -data_temp['Close'].diff(periods=-1)
        data_temp.dropna(inplace=True)
        df = pd.concat([df, data_temp], ignore_index=True)
    return df