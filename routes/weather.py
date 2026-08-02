from flask import Blueprint, request, jsonify
from services.weather_service import get_weather

weather_bp = Blueprint("weather", __name__)

@weather_bp.route("/weather", methods=["GET"])
def weather():

    city = request.args.get("city")
    print("Received city:", city)

    if not city:
        return jsonify({"error": "City parameter is required"}), 400

    data = get_weather(city)

    return jsonify(data)