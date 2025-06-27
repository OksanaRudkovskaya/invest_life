# config_model.py
import torch
MODEL_PATH = "./models/lstm_model_mini_with_config.pth"
SCALERS_PATH = r"C:\Users\zarocool\Documents\Обучение_ML\Homework\8HW\scalers_lstm_mini.pkl"
INPUT_DATA_PATH = r"C:\Users\zarocool\Documents\Обучение_ML\Homework\8HW\Investing_data_rus_exp.csv"

WINDOW_SIZE = 30

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"