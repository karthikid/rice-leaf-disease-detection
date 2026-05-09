import numpy as np
from PIL import Image
from .model import model

CLASSES = [
    'Bacterial Leaf Blight',
    'Brown Spot',
    'Healthy Rice Leaf',
    'Leaf Blast',
    'Leaf scald',
    'Narrow Brown Leaf Spot',
    'Rice Hispa',
    'Sheath Blight'
]

PRECAUTIONS = {
    'Bacterial Leaf Blight': "Use resistant varieties, avoid excess nitrogen fertilizers, and ensure proper drainage.",
    'Brown Spot': "Apply fungicides, maintain proper soil nutrition, and avoid water stress.",
    'Healthy Rice Leaf': "No disease detected. Maintain proper irrigation and fertilization practices.",
    'Leaf Blast': "Use resistant seeds, apply fungicides, and avoid excessive nitrogen use.",
    'Leaf scald': "Improve field sanitation and apply recommended fungicides.",
    'Narrow Brown Leaf Spot': "Ensure balanced fertilization and apply fungicides if needed.",
    'Rice Hispa': "Use insecticides and remove affected leaves to prevent spread.",
    'Sheath Blight': "Maintain proper spacing, reduce humidity, and apply fungicides."
}

def preprocess_image(image_file):
    image = Image.open(image_file).convert("RGB")
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

def predict_disease(image_file):
    img = preprocess_image(image_file)

    prediction = model.predict(img)

    class_index = np.argmax(prediction)
    confidence = float(np.max(prediction))

    disease = CLASSES[class_index]
    precaution = PRECAUTIONS[disease]

    return disease, round(confidence * 100, 2), precaution