# utils.py
import torch
from src.services.analitics_old.model_lstm import LSTMModel
from model_lstm import LSTMModel

def load_model(model_path, device="cpu"):
    """
    Загружает модель из чекпоинта.
    Если input_dim не указан, берёт его из чекпоинта.
    """
    checkpoint = torch.load(model_path, map_location='cpu')
    features = checkpoint['features']

    model = LSTMModel(
        input_dim=checkpoint['input_dim'],
        hidden_dim=checkpoint['hidden_dim'],
        num_layers=checkpoint['num_layers'],
        output_dim=checkpoint['output_dim'],
        dropout=checkpoint.get('dropout', 0.2)
    )

    model.load_state_dict(checkpoint['model_state_dict'])
    model.to(device)
    model.eval()

    return model, features


def predict_last_row(
    df,
    model,
    scalers,
    features,
    window=30,
    device="cpu"
):
    """
    Предсказывает класс и вероятности для последней строки датафрейма  у каждого тика
    """
    tic = df['tic'].iloc[0]
    if tic not in scalers:
        raise ValueError(f"Нет скалера для тикера '{tic}'. Модель не обучалась на этом тикере.")

    scaler = scalers[tic]
    df = df.sort_values('Date')
    relevant_data = df.iloc[-window:].copy()
    X_unscaled = relevant_data[features].values

    # Нормализация
    X_scaled = scaler.transform(X_unscaled)



    X_tensor = torch.tensor(X_scaled, dtype=torch.float32).unsqueeze(0).to(device)  # [1, window, n_features]

    # Предсказание
    with torch.no_grad():
        outputs = model(X_tensor)
        probs = torch.softmax(outputs, dim=1)
        _, preds = torch.max(outputs, 1)

    return preds.item(), probs.numpy()[0]