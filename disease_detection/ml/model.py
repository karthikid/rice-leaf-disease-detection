import os
from tensorflow.keras.models import load_model
from tensorflow.keras.layers import Dense

# ---- Fix for Keras quantization_config issue ----
original_from_config = Dense.from_config

@classmethod
def patched_from_config(cls, config):
    config.pop("quantization_config", None)
    return original_from_config(config)

Dense.from_config = patched_from_config

# ---- Load Model ----
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "rice_model.h5"
)

model = load_model(
    MODEL_PATH,
    compile=False
)