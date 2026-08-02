from flask import Blueprint,request,jsonify

from services.weather_service import get_weather
from services.health_service import calculate_health_index


health_bp = Blueprint(
    "health",
    __name__
)


@health_bp.route("/health-index")
def health_index():

    city=request.args.get("city")


    if not city:
        return jsonify({
            "error":"City required"
        }),400


    weather=get_weather(city)


    result=calculate_health_index(weather)


    return jsonify({
        **weather,
        **result
    })