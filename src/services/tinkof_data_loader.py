import asyncio
import pandas as pd
from datetime import datetime, timedelta, timezone
from tinkoff.invest import AsyncClient, CandleInterval
from tinkoff.invest.utils import now


# Получаем данные с сайта тинькоф инвестиции
async def fetch_candles_by_figi(figi: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    async with AsyncClient(TOKEN) as client:
        all_candles = []
        current_date = start_date

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
                        "time": candle.time,
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

        return pd.DataFrame(all_candles)


async def get_candles(figies: list, start_date: datetime, end_date: datetime):
    start_date = datetime(2018, 1, 1, tzinfo=timezone.utc)
    end_date = now()

    tasks = []
    for figi in figies.values():
        tasks.append(fetch_candles_by_figi(figi, start_date, end_date))

    results = await asyncio.gather(*tasks)

    combined_df = pd.concat(results)

    return combined_df


if __name__ == "__main__":
    figies = {
        "SBER": "BBG004730N88",
        "GAZP": "BBG004730RP0",
        "AAPL": "BBG000B9XRY4",  # Apple
        "MSFT": "BBG000BPH459",  # Microsoft
    }
    TOKEN = 't.f0ansg-0lg5F_oqmhMm_xl0DECuv9LXxEXTo30tQCC8PLjO6YaeK19vuGuQEqxQFiRWAmp92BENN2QMV1vRXiQ'
    start_date = start_date = datetime(2018, 1, 1, tzinfo=timezone.utc)
    end_date = now()
    df = asyncio.run(get_candles(figies, start_date, end_date))

