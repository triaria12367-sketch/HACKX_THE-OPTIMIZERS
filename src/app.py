from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from datetime import datetime
import random

# ----------------------------------------------------------------------
# 🔧 Base Directories
# ----------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RECORD_DIR = os.path.join(BASE_DIR, "recordings")
os.makedirs(RECORD_DIR, exist_ok=True)

# ----------------------------------------------------------------------
# ⚙️ Flask Initialization
# ----------------------------------------------------------------------
app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")
CORS(app)

# ----------------------------------------------------------------------
# 🏠 Home Route
# ----------------------------------------------------------------------
@app.route("/")
def home():
    return send_from_directory(BASE_DIR, "demo.html")

# ----------------------------------------------------------------------
# 🔍 Status Route
# ----------------------------------------------------------------------
@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "online", "api_status": "ready"})

# ----------------------------------------------------------------------
# 💬 Simple Chatbot (Demo)
# ----------------------------------------------------------------------
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if "safe" in user_message.lower():
        reply = "Yes, safety first! Stick to well-lit and populated areas."
    elif "police" in user_message.lower():
        reply = "The nearest police station can be found via emergency services (dial 112/100)."
    else:
        reply = "I’m your OmniDimension AI. Stay safe!"

    return jsonify({"reply": reply})

# ----------------------------------------------------------------------
# 🎥 Video Upload Endpoint (for Guardian)
# ----------------------------------------------------------------------
@app.route("/upload_video", methods=["POST"])
def upload_video():
    """
    Receives a recorded video Blob from the frontend via FormData.
    Saves it inside /recordings/ folder.
    """
    try:
        if "video" not in request.files:
            return jsonify({"status": "error", "message": "No video file found"}), 400

        video = request.files["video"]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"guardian_session_{timestamp}.webm"
        file_path = os.path.join(RECORD_DIR, filename)

        video.save(file_path)

        print(f"[INFO] 🎬 Video saved: {filename}")
        return jsonify({"status": "success", "file": filename})
    except Exception as e:
        print("❌ Error saving video:", e)
        return jsonify({"status": "error", "message": str(e)}), 500

# ----------------------------------------------------------------------
# 🌦️ AI-Powered Risk Forecast (Demo)
# ----------------------------------------------------------------------
@app.route("/forecast", methods=["POST"])
def forecast():
    """
    Predicts area-wise crime risk for the next 24 hours (demo version).
    Input JSON: { "location": "Ahmedabad", "weather": "Rainy" }
    Output: risk percentage + safe-travel suggestion.
    """
    data = request.get_json()
    location = data.get("location", "Unknown")
    weather = data.get("weather", "Clear")

    # Basic demo logic (replace with ML model in real version)
    base_risk = random.randint(20, 70)
    if weather.lower() in ["rainy", "storm", "fog"]:
        base_risk += 15
    elif weather.lower() in ["sunny", "clear"]:
        base_risk -= 5

    risk_score = max(0, min(100, base_risk))

    if risk_score < 30:
        suggestion = "Low risk — travel anytime safely."
    elif risk_score < 60:
        suggestion = "Moderate risk — prefer 7 AM – 7 PM."
    else:
        suggestion = "High risk — avoid late nights, travel in groups."

    result = {
        "location": location,
        "weather": weather,
        "risk_score": risk_score,
        "forecast_window": "Next 24 Hours",
        "safe_travel_suggestion": suggestion
    }
    print(f"[FORECAST] {result}")
    return jsonify(result)

# ----------------------------------------------------------------------
# 🚀 Run Server
# ----------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)