from typing import Dict, Any, List, Tuple

def calculate_climate_health_index(
    aqi: float = 65.0,
    temp: float = 26.0,
    uv: float = 5.0,
    pollen: float = 25.0
) -> Dict[str, Any]:
    penalty = 0.0

    # 1. AQI Penalty
    if aqi <= 50:
        penalty += (aqi / 50.0) * 5.0
    elif aqi <= 100:
        penalty += 5.0 + ((aqi - 50.0) / 50.0) * 15.0
    elif aqi <= 200:
        penalty += 20.0 + ((aqi - 100.0) / 100.0) * 30.0
    else:
        penalty += 50.0 + ((aqi - 200.0) / 150.0) * 30.0

    # 2. Temperature Penalty (ideal comfort: 20-25°C)
    if temp > 25.0:
        penalty += (temp - 25.0) * 2.2
    elif temp < 15.0:
        penalty += (15.0 - temp) * 1.5

    # 3. UV Penalty
    penalty += (uv * 2.8)

    # 4. Pollen / Allergen Penalty
    penalty += (pollen * 0.25)

    raw_score = 100.0 - penalty
    final_score = max(0, min(100, round(raw_score)))

    if final_score >= 80:
        label = "Optimal"
        desc = "Climate conditions are highly favorable for human respiratory, cardiovascular, and immunological systems."
        recommendation = "Outdoor activities are safe. Ideal time for exercise and ventilation."
    elif final_score >= 60:
        label = "Fair"
        desc = "Acceptable climate comfort. Sensitive individuals with chronic asthma or heart diseases should monitor localized symptoms."
        recommendation = "Stay hydrated and avoid prolonged midday peak exposure."
    elif final_score >= 40:
        label = "Cautionary"
        desc = "Moderate climate stress. Ambient temperatures, high UV, or particulate pollution may cause fatigue and respiratory congestion."
        recommendation = "Limit intense outdoor exertion. Wear UV and particulate protection."
    else:
        label = "Hazardous"
        desc = "Severe ambient risk. High heat indices or intense microparticle concentrations pose systemic health threats. Limit exposure."
        recommendation = "Avoid outdoor activity. Stay in climate-controlled indoor spaces and monitor health."

    return {
        "climate_health_index": final_score,
        "risk_level": label,
        "recommendation": recommendation,
        "description": desc,
        "breakdown": {
            "aqi_impact": round(min(80.0, penalty), 1),
            "temp_impact": round(max(0.0, (temp - 25.0) * 2.2 if temp > 25 else (15.0 - temp) * 1.5 if temp < 15 else 0.0), 1),
            "uv_impact": round(uv * 2.8, 1),
            "pollen_impact": round(pollen * 0.25, 1)
        }
    }

def calculate_personalized_risk(
    profile: Dict[str, Any],
    environment: Dict[str, Any]
) -> Dict[str, Any]:
    base_score = 20.0
    aqi = float(environment.get("aqi", 68.0))
    temp = float(environment.get("temp", 24.0))
    uv = float(environment.get("uv", 4.0))

    # Environmental additions
    base_score += (aqi / 3.0)
    base_score += max(0.0, (temp - 22.0) * 1.5)
    base_score += (uv * 3.0)

    modifiers: List[str] = []
    age = int(profile.get("age", 30))
    occupation = str(profile.get("occupation", "indoor")).lower()
    conditions = profile.get("conditions", {})

    if age < 12:
        base_score += 12.0
        modifiers.append("Sensitive age group (Child)")
    elif age > 65:
        base_score += 20.0
        modifiers.append("Vulnerable age group (Senior Citizen)")

    if occupation == "outdoor":
        base_score += 15.0
        modifiers.append("High exposure due to outdoor occupation")
    else:
        modifiers.append("Indoor baseline work profile")

    if conditions.get("asthma"):
        base_score += 25.0
        modifiers.append("Pre-existing Asthma / Bronchial Hyperresponsiveness")
    if conditions.get("cardiovascular"):
        base_score += 25.0
        modifiers.append("Pre-existing Cardiovascular / Heart Disease")
    if conditions.get("allergies"):
        base_score += 10.0
        modifiers.append("Seasonal Allergies (Pollen / Spores)")
    if conditions.get("copd"):
        base_score += 30.0
        modifiers.append("Pre-existing COPD risk")

    final_score = min(100, max(0, round(base_score)))

    if final_score > 70:
        level = "Extreme"
        color = "text-red-700 bg-red-50 border-red-200"
        ring = "border-red-500"
    elif final_score > 45:
        level = "Moderate"
        color = "text-orange-600 bg-orange-50 border-orange-200"
        ring = "border-orange-500"
    else:
        level = "Low"
        color = "text-green-600 bg-green-50 border-green-200"
        ring = "border-green-500"

    return {
        "score": final_score,
        "level": level,
        "color": color,
        "ring": ring,
        "modifiers": modifiers,
        "source": "FastAPI Climate-Health Predictive Engine"
    }

def calculate_safe_time_slots(
    profile: Dict[str, Any],
    base_temp: float = 24.0,
    base_aqi: float = 65.0
) -> List[Dict[str, Any]]:
    # 6 Standard Hourly Windows
    raw_slots = [
        {"time": "06:00", "label": "Early Morning", "temp": round(base_temp - 5.0, 1), "aqi": round(base_aqi * 0.7), "uv": 1.0, "wind": 8.0},
        {"time": "08:00", "label": "Morning Commute", "temp": round(base_temp - 2.0, 1), "aqi": round(base_aqi * 0.8), "uv": 2.0, "wind": 10.0},
        {"time": "12:00", "label": "Midday Peak", "temp": round(base_temp + 5.0, 1), "aqi": round(base_aqi * 1.15), "uv": 8.0, "wind": 12.0},
        {"time": "15:00", "label": "Late Afternoon", "temp": round(base_temp + 4.0, 1), "aqi": round(base_aqi * 1.25), "uv": 5.0, "wind": 14.0},
        {"time": "18:00", "label": "Evening", "temp": round(base_temp - 1.0, 1), "aqi": round(base_aqi * 0.9), "uv": 1.0, "wind": 9.0},
        {"time": "21:00", "label": "Night", "temp": round(base_temp - 4.0, 1), "aqi": round(base_aqi * 0.75), "uv": 0.0, "wind": 7.0}
    ]

    evaluated_slots = []
    conditions = profile.get("conditions", {})
    age = int(profile.get("age", 30))
    occupation = str(profile.get("occupation", "indoor")).lower()

    for s in raw_slots:
        penalty = (s["aqi"] / 2.5)
        if s["temp"] > 27.0:
            penalty += (s["temp"] - 27.0) * 4.0
        penalty += (s["uv"] * 5.0)

        if conditions.get("asthma") and s["aqi"] > 60:
            penalty += 25.0
        if conditions.get("allergies") and s["temp"] > 25.0:
            penalty += 10.0
        if occupation == "outdoor":
            penalty += 10.0
        if age > 65:
            penalty += 15.0

        if penalty > 65:
            status = "Critical"
            color = "bg-red-500"
            desc = "High pollutant & thermal loading."
        elif penalty > 40:
            status = "Caution"
            color = "bg-orange-400"
            desc = "Moderate risk. Wear protection/mask."
        else:
            status = "Safe"
            color = "bg-green-500"
            desc = "Excellent time for activities."

        evaluated_slots.append({
            "time": s["time"],
            "label": s["label"],
            "temp": s["temp"],
            "aqi": s["aqi"],
            "uv": s["uv"],
            "wind": s["wind"],
            "status": status,
            "color": color,
            "desc": desc
        })

    return evaluated_slots
