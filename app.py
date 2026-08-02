from flask import Flask
from flask_cors import CORS

from routes.weather import weather_bp
from routes.health import health_bp
from routes.chat import chat_bp

app = Flask(__name__)
CORS(app)

app.register_blueprint(weather_bp, url_prefix="/api")
app.register_blueprint(health_bp, url_prefix="/api")
app.register_blueprint(chat_bp, url_prefix="/api")


@app.route("/")
def home():
    return {
        "status": "success",
        "message": "ClimaCare AI Backend Running 🚀"
    }

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)