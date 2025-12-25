import { useState } from "react";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  function handleImageChange(e) {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  }

  async function analyzePlant() {
    if (!image) {
      alert("Please upload a leaf image first");
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append("image", image);

    try {
      const res = await fetch("http://localhost:8000/predict", {
        method: "POST",
        body: formData
      });

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert("Failed to connect to backend");
    } finally {
      setLoading(false);
    }
  }

  const resultClass =
    result?.diseaseName === "Tomato Healthy" ? "healthy" : "disease";

  return (
    <div className="app-container">
      <h1>Plant Health Monitoring System</h1>
      <p className="subtitle">
        AI-based Tomato Leaf Disease Detection using CNN
      </p>

      <div className="upload-box">
        <input type="file" accept="image/*" onChange={handleImageChange} />
      </div>

      {preview && <img src={preview} alt="preview" className="preview-img" />}

      <button
        className="analyze-btn"
        onClick={analyzePlant}
        disabled={loading}
      >
      Analyze Plant Health
      </button>

      {loading && (
      <div className="spinner-container">
        <div>
          <div className="spinner"></div>
          <div className="loading-text">Analyzing image...</div>
        </div>
      </div>
      )}

      {result && (
        <div className={`result-card ${resultClass}`}>
          <h2>Disease Result</h2>

          <p><strong>Name:</strong> {result.diseaseName}</p>
          <p className="confidence">
            <strong>Confidence:</strong> {result.confidenceScore}
          </p>

          <p className="section-title"><strong>Description</strong></p>
          <p>{result.description}</p>

          <p className="section-title"><strong>Treatment Steps</strong></p>
          <ul>
            {result.treatmentSteps.map((step, i) => (
              <li key={i}>{step}</li>
            ))}
          </ul>

          <p className="section-title"><strong>Prevention Tips</strong></p>
          <ul>
            {result.preventionTips.map((tip, i) => (
              <li key={i}>{tip}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
