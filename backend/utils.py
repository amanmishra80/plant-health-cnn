import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH = os.path.join("model", "plant_model.h5")

# Load trained model
model = load_model(MODEL_PATH)

# IMPORTANT: Order MUST match training folders
CLASS_NAMES = [
    "Tomato Early Blight",
    "Tomato Late Blight",
    "Tomato Healthy"
]

def predict_disease(img_path):
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    predictions = model.predict(img_array)
    class_index = np.argmax(predictions)
    confidence = float(np.max(predictions))

    return CLASS_NAMES[class_index], confidence
