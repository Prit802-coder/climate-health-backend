from typing import Optional, Dict, Any

def generate_chat_reply(message: str, context: Optional[Dict[str, Any]] = None) -> str:
    msg = message.strip().lower()
    ctx = context or {}
    city = ctx.get("currentCity") or "your area"
    w_data = ctx.get("weatherData") or {}
    temp = w_data.get("temperature") or w_data.get("temp") or 28
    aqi = w_data.get("aqi") or 75

    # 1. Asthma & Humidity / Respiratory queries
    if any(k in msg for k in ["asthma", "breathing", "inhaler", "wheezing", "bronchial"]):
        return (
            f"**Clinical Respiratory Directive for {city} (Current Temp: {temp}°C, AQI: {aqi})**:\n\n"
            f"• **Airway Sensitivity**: Fine particulates (PM2.5) and sudden temperature fluctuations irritate tracheobronchial mucosa, triggering bronchospasms.\n"
            f"• **Inhaler Access**: Always carry your fast-acting rescue bronchodilator (e.g. Albuterol/Salbutamol).\n"
            f"• **Indoor Environment**: Keep windows closed during traffic peaks (08:00–10:00 & 18:00–20:00). Maintain indoor relative humidity between 40% and 50% using HEPA filtration.\n"
            f"• **When to Seek Urgent Care**: Continuous breathlessness, retractions, or lack of relief 15 minutes post-inhaler requires emergency evaluation."
        )

    # 2. Outdoor Running / Exercise / Sports safety
    elif any(k in msg for k in ["run", "running", "jog", "exercise", "workout", "gym", "safe outside", "outside"]):
        if aqi > 100 or temp > 33:
            return (
                f"**Exercise Advisory in {city} (Temp: {temp}°C, AQI: {aqi})**: **Not Recommended Outdoors Today**\n\n"
                f"• **Ventilatory Burden**: Heavy aerobic exertion increases minute ventilation by 500%, carrying micro-toxins deep into alveolar capillary beds.\n"
                f"• **Thermal Stress**: High temperatures accelerate fluid loss and trigger peripheral vasodilation, spiking cardiac strain.\n"
                f"• **Alternative**: Switch to an indoor cardio session, gym treadmill, or stretch routine in air-conditioned spaces."
            )
        else:
            return (
                f"**Exercise Advisory in {city} (Temp: {temp}°C, AQI: {aqi})**: **Favorable for Outdoor Training**\n\n"
                f"• **Air Quality**: AQI is within acceptable physiological parameters for cardiovascular workouts.\n"
                f"• **Hydration**: Drink 250ml of water every 20 minutes of moderate activity.\n"
                f"• **Sun Protection**: Apply broad-spectrum SPF 30+ sunscreen if working out between 10:00 AM and 04:00 PM."
            )

    # 3. Heat exhaustion / Sunstroke / Heatwave
    elif any(k in msg for k in ["heat", "exhaustion", "stroke", "sunstroke", "dehydration", "cramp"]):
        return (
            f"**Thermal Stress & Heat Illness Prevention ({city} Baseline: {temp}°C)**:\n\n"
            f"• **Early Symptoms**: Palpitations, dizziness, excessive sweating, muscle cramps, headache, or nausea.\n"
            f"• **Emergency Action**: Move to shade or air conditioning immediately, loosen tight clothing, and consume oral rehydration solutions (ORS) or electrolyte water.\n"
            f"• **Avoid**: Caffeinated or high-sugar sodas, which act as diuretics and exacerbate intravascular volume depletion."
        )

    # 4. Air Quality / AQI / Particulate matter / Smog
    elif any(k in msg for k in ["aqi", "air quality", "smog", "pollution", "pm2.5", "pm10", "mask", "n95"]):
        return (
            f"**Air Quality Clinical Analysis for {city} (AQI: {aqi})**:\n\n"
            f"• **Current Classification**: {w_data.get('aqi_label', 'Moderate to High particulate levels')}.\n"
            f"• **Protection**: When commuting outdoors in AQI > 100, wear a well-fitted certified N95 / FFP2 respirator mask. Cloth masks do not filter fine sub-micron PM2.5 particles.\n"
            f"• **Eye Care**: Wear protective eyeglasses or sunglasses to reduce chemical conjunctivitis caused by ozone and nitrogen oxides."
        )

    # 5. Cardiovascular / Heart disease
    elif any(k in msg for k in ["heart", "cardio", "cardiovascular", "hypertension", "blood pressure"]):
        return (
            f"**Cardiovascular Health Warning in {city}**:\n\n"
            f"• **Mechanism**: Inhaled ultra-fine PM2.5 triggers systemic arterial vasoconstriction and platelet aggregation, raising acute myocardial infarction risks.\n"
            f"• **Guidelines**: Strictly avoid strenuous outdoor labor during peak pollution hours. Maintain prescribed antihypertensives and monitor resting pulse rates daily."
        )

    # 6. Allergies / Pollen / Eyes
    elif any(k in msg for k in ["allergy", "allergies", "pollen", "itch", "sneez", "rash"]):
        return (
            f"**Allergen & Environmental Dermatitis Guidance**:\n\n"
            f"• **Pollen Counts**: Spores peak in mid-mornings on windy days. Keep automobile windows closed.\n"
            f"• **Post-Exposure**: Wash face and eyes with saline wash immediately after returning from outdoor environments.\n"
            f"• **Therapy**: Antihistamines and lubricating ocular drops provide first-line symptom relief for allergic rhinitis."
        )

    # 7. Default friendly medical companion
    else:
        return (
            f"Hello! I am your ClimaCare Clinical Health Companion for **{city}**.\n\n"
            f"Current Local Conditions: **{temp}°C**, AQI **{aqi}**.\n\n"
            f"You can ask me questions like:\n"
            f"• *Is it safe to run or exercise outdoors today?*\n"
            f"• *How do I protect my asthma in high humidity?*\n"
            f"• *What are the first symptoms of heat exhaustion?*\n"
            f"• *How does current PM2.5 affect heart disease patients?*"
        )
