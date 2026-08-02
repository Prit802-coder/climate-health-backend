from flask import Blueprint, request, jsonify

chat_bp = Blueprint("chat", __name__)

@chat_bp.route("/chat", methods=["POST"])
def chat():

    data = request.json
    message = data.get("message", "").lower()

    if "outside" in message:
        reply = "The weather is safe today. You can go outside, but stay hydrated."

    elif "heat" in message:
        reply = "Avoid direct sunlight between 12 PM and 3 PM."

    elif "rain" in message:
        reply = "Carry an umbrella. Roads may be slippery."

    elif "aqi" in message:
        reply = "Current AQI is acceptable for most people."

    else:
        reply = "I'm your ClimaCare AI assistant. Ask me about weather or health."

    return jsonify({
        "reply": reply
    })