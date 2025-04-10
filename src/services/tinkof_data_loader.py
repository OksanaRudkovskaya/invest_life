import asyncio
from datetime import datetime, timedelta, time
from tinkoff.invest import AsyncClient, CandleInterval



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
                        "date": candle.time.replace(tzinfo=None),
                        "figi": figi,
                        "open": float(candle.open.units + candle.open.nano / 1e9),
                        "high": float(candle.high.units + candle.high.nano / 1e9),
                        "low": float(candle.low.units + candle.low.nano / 1e9),
                        "close": float(candle.close.units + candle.close.nano / 1e9),
                        "volume": candle.volume
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
    figis = []
    for ticker, figi in figies.items():
        tasks.append(fetch_candles_by_figi(figi, start_date, end_date, token))
        tickers.append(ticker)
        figis.append(figi)

    candles_list = await asyncio.gather(*tasks)

    df_list = []
    for ticker, figi, candles in list(zip(tickers, figis, candles_list)):
        for candle in candles:
            df_list.append({
                "date": candle["date"],
                "tic": ticker,
                "open": candle["open"],
                "high": candle["high"],
                "low": candle["low"],
                "close": candle["close"],
                "volume": candle["volume"]
            })

    return df_list


if __name__ == "__main__":
    from settings import TINKOFF_TOKEN

    figies = {
        "SBER": "BBG004730N88",
        "GAZP": "BBG004730RP0",
        "AAPL": "BBG000B9XRY4",
        "MSFT": "BBG000BPH459",
    }
    start_date = datetime(2018, 1, 1)
    end_date = datetime.combine(datetime.now().date() - timedelta(days=1), time.max).replace(tzinfo=None)
    df = asyncio.run(get_candles(figies, start_date, end_date, TINKOFF_TOKEN))