from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from utils import predict_disease

DISEASE_INFO = {
    "Tomato Early Blight": {
        "description": "Early blight is a fungal disease causing dark spots on tomato leaves.",
        "treatment": [
            "Remove infected leaves immediately",
            "Apply copper-based fungicide",
            "Avoid overhead irrigation"
        ],
        "prevention": [
            "Practice crop rotation",
            "Use disease-free seeds",
            "Maintain proper plant spacing"
        ]
    },

    "Tomato Late Blight": {
        "description": "Late blight is a serious disease causing rapid leaf decay and plant death.",
        "treatment": [
            "Remove and destroy infected plants",
            "Apply recommended fungicide",
            "Reduce moisture around plants"
        ],
        "prevention": [
            "Avoid watering leaves",
            "Ensure good air circulation",
            "Monitor plants regularly"
        ]
    },

    "Tomato Healthy": {
        "description": "The plant is healthy with no visible disease symptoms.",
        "treatment": [
            "No treatment required",
            "Continue regular care"
        ],
        "prevention": [
            "Maintain proper watering schedule",
            "Use balanced fertilizers",
            "Inspect plants regularly"
        ]
    }
}

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def home():
    return jsonify({"message": "Flask backend is running"})

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    img = request.files["image"]
    img_path = os.path.join(UPLOAD_FOLDER, img.filename)
    img.save(img_path)

    # 🔥 REAL CNN PREDICTION
    disease, confidence = predict_disease(img_path)

    info = DISEASE_INFO.get(disease, {
    "description": "Information not available",
    "treatment": [],
    "prevention": []
})

    return jsonify({
    "diseaseName": disease,
    "confidenceScore": round(confidence, 2),
    "description": info["description"],
    "treatmentSteps": info["treatment"],
    "preventionTips": info["prevention"]
})


if __name__ == "__main__":
    app.run(debug=True, port=8000)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
