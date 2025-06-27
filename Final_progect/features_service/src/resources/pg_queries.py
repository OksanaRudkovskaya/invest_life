sql_get_data = """WITH ranked_data AS (
                    SELECT
                        dttm as Date,
                        ticker as tic,
                        open,
                        high,
                        low,
                        close,
                        volume,
                        ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY dttm DESC) AS rn
                    from moex_data.candles_1d
					join moex_data.securities on id = ticker_id
                    where ticker in ('LKOH','SBER','MTSS'))
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
                    ORDER BY tic, date desc;"""