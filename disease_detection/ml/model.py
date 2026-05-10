from tensorflow.keras.models import load_model
import keras
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "rice_model.h5")

model = load_model(
    MODEL_PATH,
    compile=False,
    safe_mode=False
)