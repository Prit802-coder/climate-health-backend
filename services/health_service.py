def calculate_health_index(weather):

    temperature = weather["temperature"]
    humidity = weather["humidity"]
    condition = weather["condition"]


    score = 100


    # Temperature impact
    if temperature > 40:
        score -= 35
    elif temperature > 35:
        score -= 20
    elif temperature < 10:
        score -= 15


    # Humidity impact
    if humidity > 80:
        score -= 20
    elif humidity > 60:
        score -= 10


    # Weather impact
    if condition == "Rain":
        score -= 5

    if condition == "Thunderstorm":
        score -= 25


    score = max(0, min(score,100))


    if score >= 80:
        risk="Low"

    elif score >=50:
        risk="Moderate"

    else:
        risk="High"


    return {
        "climate_health_index":score,
        "risk_level":risk,
        "recommendation":get_advice(risk)
    }



def get_advice(risk):

    if risk=="Low":
        return "Outdoor activities are safe."

    elif risk=="Moderate":
        return "Stay hydrated and avoid long exposure."

    else:
        return "Avoid outdoor activity and monitor health."