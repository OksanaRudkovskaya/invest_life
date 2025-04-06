import pandas as pd
import yfinance as yf
#from datetime import date

# Получаем данные с сайта yahoo
def get_candles(tickers, start_date, end_date):

    data_df = pd.DataFrame()
    num_failures = 0
    for tic in tickers:
        temp_df = yf.download(
            tic,
            start=start_date,
            end=end_date,
            proxy=None,
            auto_adjust=False,
        )
        if temp_df.columns.nlevels != 1:
            temp_df.columns = temp_df.columns.droplevel(1)
        temp_df["tic"] = tic

        if len(temp_df) > 0:
            # data_df = data_df.append(temp_df)
            data_df = pd.concat([data_df, temp_df], axis=0)
        else:
            num_failures += 1

    if num_failures == len(tickers):
        raise ValueError("no data is fetched.")
    # reset the index, we want to use numbers as index instead of dates
    data_df = data_df.reset_index()
    data_df["Date"] = data_df.Date.apply(lambda x: x.strftime("%Y-%m-%d"))

    print("Shape of DataFrame: ", data_df.shape)

    df = data_df.sort_values(by=["tic", "Date"]).reset_index(drop=True)
    return df

if __name__ == "__main__":
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'NVDA', 'META']
    start_date = '2009-01-01'
    end_date = '2021-01-01'
    df = get_candles(tickers, start_date, end_date)