import pickle

import torch

from Final_progect.predict_service.src.predict.models import DataItem
from Final_progect.predict_service.model.model_lstm import LSTMModel
from Final_progect.predict_service.settings import SCALERS_PATH, MODEL_PATH


class PredictService:
    def __init__(self, device='cpu'):
        self.device = device
        with open(SCALERS_PATH, "rb") as f:
            self.scalers = pickle.load(f)

        self.model, self.features = self.load_model(MODEL_PATH, device)


    @staticmethod
    def load_model(model_path, device="cpu"):
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


    @staticmethod
    def prepare_data(data: DataItem):
        ticker = data.ticker
        data_sorted = data.sort_vectors_by_date().vectors
        vectors = [v.vector for v in data_sorted]
        return ticker, vectors

    def predict_last_row(self, data: DataItem, window=30):
        ticker, vectors = self.prepare_data(data)
        vectors = vectors[-window:]

        if ticker not in self.scalers:
            print(f"Нет скалера для тикера '{ticker}'. Модель не обучалась на этом тикере.")
            return None, None

        scaler = self.scalers[ticker]

        X_scaled = scaler.transform(vectors)
        X_tensor = torch.tensor(X_scaled, dtype=torch.float32).unsqueeze(0).to(self.device)  # [1, window, n_features]
        # Предсказание
        with torch.no_grad():
            outputs = self.model(X_tensor)
            probs = torch.softmax(outputs, dim=1)
            _, preds = torch.max(outputs, 1)

        return preds.item(), probs.numpy()[0]
