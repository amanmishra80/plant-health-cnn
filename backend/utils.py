import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH = os.path.join("model", "plant_model.h5")

model = None

CLASS_NAMES = [
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Healthy"
]

def get_model():
    global model
    if model is None:
        model = load_model(MODEL_PATH)
    return model

def predict_disease(img_path):
    model = get_model()

    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    class_index = np.argmax(predictions)
    confidence = float(np.max(predictions))

    return CLASS_NAMES[class_index], confidence