import pandas as pd
import yahoo_data_loader

# Добавим функцию по поиску выбросов исходя из разности цен
def iqr(df, ticker, col, ratio):
    # Расчет IQR для цен закрытия
    close_prices = df[df['tic'] == ticker][col]

    # Вычисление квартилей
    Q1 = close_prices.quantile(0.25)  # Первый квартиль (25-й процентиль)

    Q3 = close_prices.quantile(0.75)  # Третий квартиль (75-й процентиль)
    IQR = Q3 - Q1  # Межквартильный размах

    # Границы для выбросов
    lower_bound = Q1 - ratio * IQR
    upper_bound = Q3 + ratio * IQR

    # Поиск выбросов
    outliers = close_prices[(close_prices < lower_bound) | (close_prices > upper_bound)]

    return Q1, Q3, IQR, lower_bound, upper_bound, len(outliers)




def clear_data(df):
    # Заполняем пропуски последним значением
    df.fillna(method='ffill', inplace=True)

    # Добавляем столбец с отношением цены закрытия текущего дня и предыдущего
    df['pr_close'] = df.groupby('tic')['Close'].transform(lambda x: (x - x.shift(1)) / x * 100)


    # Добавим выбросы в отдельный столбец
    for ticker in df['tic'].unique:

        Q1, Q3, IQR, lower_bound, upper_bound, count_out = iqr(df, ticker, 'pr_close', 1.5)
        # Находим персентиль объема торгов для каждого дня
        df.loc[(df['tic'] == ticker), 'Volume_perc'] = df.loc[(df['tic'] == ticker), 'Volume'].rank(pct=True)
        # Обозначаем выбросы
        df.loc[(df['tic'] == ticker) & (df['pr_close'] < lower_bound) & (df['Volume_perc'] < 0.4), 'Out_bound'] = True
        df.loc[(df['tic'] == ticker) & (df['pr_close'] > upper_bound) & (df['Volume_perc'] < 0.4), 'Out_bound'] = True
    return df

if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META']
    start_date = '2009-01-01'
    end_date = '2021-01-01'
    df = yahoo_data_loader.get_candles(tickers, start_date, end_date)
    df = clear_data(df)
