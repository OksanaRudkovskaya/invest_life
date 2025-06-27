import os
import torch
from config_model import FEATURES, WINDOW_SIZE, MODEL_PATH, INPUT_DIM, HIDDEN_DIM, NUM_LAYERS, OUTPUT_DIM, DEVICE, SCALERS_PATH

path = r"C:\Users\zarocool\Documents\Обучение_ML\Homework\8HW\scalers_lstm_mini.pkl"

if os.path.exists(path):
    print("Путь существует!")
else:
    print("Путь не найден.")



checkpoint = torch.load(MODEL_PATH, map_location='cpu')

print(checkpoint)