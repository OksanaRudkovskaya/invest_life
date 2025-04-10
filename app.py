import src.services.tinkof_data_loader as tdl # Загрузка из Т-инвестиций
import src.services.clear_data_service as clr #Очистка данных, нахождение аномалий
import src.services.feature_service as ft # Добаление тех.индикаторов
import asyncio
import pandas as pd
from datetime import datetime, timedelta, time

from src.connectors.pg_conn import PgConnector #Для подключения к БД
from settings import * # Здесь хранятся данные для подключения к БД и токен

figies = {
    "SBER": "BBG004730N88",
    "GAZP": "BBG004730RP0",
    "AAPL": "BBG000B9XRY4",
    "MSFT": "BBG000BPH459",
}

# Подсоединяемся к БД
postgres = PgConnector(PG_DATABASE, PG_USER, PG_PASSWORD, PG_HOST, PG_PORT)

try:
    # Забираем данные из базы, чтобы получить последний день загрузки и в дальнейшем рассчитать тех.индикаторы
    hist_df = pd.DataFrame(postgres.get_data('select date, tic, open, high, low, close, volume from t_real_data.trading_data'))

    # Определяем последний записанный в базу день
    if hist_df.empty :
        start_date = datetime(2018, 1, 1)
    else:
        start_date = hist_df['date'].max() + timedelta(days = 1)
    end_date = datetime.combine(datetime.now().date() - timedelta(days=1), time.max).replace(tzinfo=None)

    # Достаем из Тинькоф инвестиций данные по акциям
    data = asyncio.run(tdl.get_candles(figies, start_date, end_date, TINKOFF_TOKEN))

    # Записываем в базу данных реальные данные. С пропусками и всем что есть, чтобы не перезагружать на случай изменения логики
    postgres.insert_data("t_real_data", "trading_data", data)

    # Объединяем данные вновь полученные со старыми на случай наличия пропусков во вновь загруженных данных и для расчета фичей
    # Выбросы я решила не удалять и не исправлять, потому что для записи в базу нужны реальные данные, а для обучения модели нужен анализ каждой аномалии, и точно не автоматическая перезаливка.

    df = clr.clear_data(pd.concat([hist_df, pd.DataFrame(data)], ignore_index=True).sort_values(by=["date", "tic"]))

    # Создаем новые признаки в данных, тех.индикаторы
    df = ft.feature(df)

    # Записываем откорректированные новые данные с признаками в БД

    postgres.insert_data("t_real_data", "trading_data_feature", df[df['date']>=start_date].to_dict('records'))


finally:
    postgres.disconnect()



