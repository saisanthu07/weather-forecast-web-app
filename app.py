from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")

limiter = Limiter(
    key_func=get_remote_address,
    app=app,
    default_limits=["100 per hour"]
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/weather")
@limiter.limit("10 per minute")
def weather():
    city = request.args.get("city")

    if not city:
        return jsonify({"error": "City is required"}), 400

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("cod") != 200:
            return jsonify({"error": data.get("message", "Invalid city")}), 404

        return jsonify({
            "city": data["name"],
            "temp": round(data["main"]["temp"]),
            "condition": data["weather"][0]["description"].title(),
            "humidity": data["main"]["humidity"],
            "wind": data["wind"]["speed"]
        })

    except requests.RequestException:
        return jsonify({"error": "Weather service unavailable"}), 500


if __name__ == "__main__":
    app.run(debug=True)
