import asyncio
from datetime import datetime, timedelta, time
from tinkoff.invest import AsyncClient, CandleInterval, Client, InstrumentStatus
from feature_service import feature


# Получаем данные с сайта тинькоф инвестиции
async def fetch_candles_by_figi(figi: str, start_date: datetime, end_date: datetime, token: str) -> list:
    async with AsyncClient(token) as client:
        all_candles = []
        current_date = start_date
        print(current_date,end_date)
        while current_date < end_date:

            next_date = min(current_date + timedelta(days=365), end_date)

            try:
                candles = await client.market_data.get_candles(
                    figi=figi,
                    from_=current_date,
                    to=next_date,
                    interval=CandleInterval.CANDLE_INTERVAL_DAY
                )

                for candle in candles.candles:
                    all_candles.append({
                        "Date": candle.time.replace(tzinfo=None),
                        "figi": figi,
                        "Open": float(candle.open.units + candle.open.nano / 1e9),
                        "High": float(candle.high.units + candle.high.nano / 1e9),
                        "Low": float(candle.low.units + candle.low.nano / 1e9),
                        "Close": float(candle.close.units + candle.close.nano / 1e9),
                        "Volume": candle.volume
                    })

                print(
                    f"Загружено {len(candles.candles)} свечей для {figi} ({current_date.date()} - {next_date.date()})")
                current_date = next_date + timedelta(days=1)

            except Exception as e:
                print(f"Ошибка для {figi}: {str(e)}")
                break

        return all_candles


async def get_candles(figies: dict, start_date: datetime, end_date: datetime, token: str):
    tasks = []
    tickers = []
    currencies = []
    figis = []
    for figi, data in figies.items():
        ticker = data['ticker']
        currency = data['currency']
        tasks.append(fetch_candles_by_figi(figi, start_date, end_date, token))
        tickers.append(ticker)
        figis.append(figi)
        currencies.append(currency)

    candles_list = await asyncio.gather(*tasks)

    df_list = []
    for ticker, figi, candles, currencies in list(zip(tickers, figis, candles_list, currency)):
        for candle in candles:
            df_list.append({
                "Date": candle["Date"],
                "tic": ticker,
                "cur": currency,
                "Open": candle["Open"],
                "High": candle["High"],
                "Low": candle["Low"],
                "Close": candle["Close"],
                "Volume": candle["Volume"]
            })

    return df_list


if __name__ == "__main__":
    import pandas as pd
    from settings import TINKOFF_TOKEN

    with Client(TINKOFF_TOKEN) as client:
        shares = client.instruments.shares(instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE)
        shares_df = pd.DataFrame(shares.instruments)

        shares_df = shares_df[['figi', 'ticker', 'currency']]
        shares_df = shares_df[shares_df['currency'] == 'rub'].reset_index(drop=True)

    figies = shares_df.set_index('figi')[['ticker', 'currency']].to_dict(orient='index')

    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=50)
    #start_date = today()#datetime(2025, 6, 1)
    #end_date = datetime.combine(datetime.now().date() - timedelta(days=1), time.max).replace(tzinfo=None)
    df = asyncio.run(get_candles(figies, start_date, end_date, TINKOFF_TOKEN))
    df = pd.DataFrame(df)
    print(len(df))
    df = feature(df)

    df.to_csv(r'C:\Users\zarocool\Documents\Обучение_ML\Homework\8HW\Investing_data.csv', index=False)


