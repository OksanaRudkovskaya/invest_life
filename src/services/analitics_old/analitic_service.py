import pandas as pd
import json
import pickle
import sklearn
from utils import predict_last_row, load_model
from config_model import WINDOW_SIZE, MODEL_PATH, INPUT_DATA_PATH, DEVICE, SCALERS_PATH
from src.services.feature_service import feature as ft

import warnings
warnings.filterwarnings("ignore")

def batch_predict(data: dict, DEVICE = 'cpu'):

    df = pd.DataFrame(data["data"])
    with open(SCALERS_PATH, "rb") as f:
        scalers = pickle.load(f)


    model, features = load_model(MODEL_PATH, DEVICE)

    """
    Делает предсказание для каждого тикера из датафрейма

    Args:
        data : исходная форма json с колонкой 'tic'
        model: обученная модель
        scalers (dict): словарь {tic: MinMaxScaler}

    Returns:
        List[Dict]: JSON-совместимый список с предсказаниями
    """
    results = []

    for tic in df['tic'].unique():
        df_tic = df[df['tic'] == tic]

        try:
            prediction, probabilities = predict_last_row(
                df_tic,
                model,
                scalers=scalers,
                features=features,
                window=WINDOW_SIZE
            )

            # Переводим вероятности в проценты
            probs_percent = [int(round(p * 100, 1)) for p in probabilities]

            results.append({
                "tic": tic,
                "prediction": int(prediction),
                "probabilities_percent": probs_percent
            })

        except Exception as e:
            print(f"Ошибка при обработке тикера '{tic}': {e}")
            continue

    return results


if __name__ == "__main__":

    # Чтение данных
#    df = pd.read_csv(INPUT_DATA_PATH)
    data = {
        "data": json.loads(pd.read_csv(INPUT_DATA_PATH).to_json(orient='records'))
    }
#    df = ft(df)

    # Предсказание по всем тикерам
    predictions = batch_predict(data, DEVICE)

    # Вывод результата в JSON
    print(predictions)