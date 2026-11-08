# ClimaCare AI — FastAPI Backend Service

A high-performance Python FastAPI backend for the **Climate Health Advisory System**.

## 🚀 Key Features

1. **Authentication & User Management**:
   - JWT-based authentication with bcrypt password hashing.
   - User registration (`POST /api/auth/register`), login (`POST /api/auth/login`), profile retrieval (`GET /api/auth/me`), and personal bio-risk profile updates (`PUT /api/auth/profile`).
2. **Real Weather & Air Quality Integration**:
   - Live OpenWeather Current Weather (`/data/2.5/weather`) and Multi-Pollutant Air Quality (`/data/2.5/air_pollution`) with geocoding.
   - Comprehensive Indian CPCB AQI calculation converting raw concentrations ($\text{PM}_{2.5}$, $\text{PM}_{10}$, $\text{NO}_2$, $\text{SO}_2$, $\text{CO}$, $\text{O}_3$) to sub-indices and overall AQI category.
3. **Climate Health Index & Bio-Risk Prediction**:
   - Multi-stressor Composite Climate Health Index ($0$ to $100$) combining particulate loads, heat indices, UV radiation, and pollen/allergens.
   - Dynamic Bio-Risk Profile calculation factoring in age groups ($<12$ Child, $>65$ Senior), occupation exposure (Indoor vs Outdoor), and pre-existing chronic conditions (Asthma, Cardiovascular, Allergies, COPD).
   - 24-Hour Safe Time Activity Planner evaluating optimal hourly windows for jogging, outdoor labor, and commuting.
4. **Ward-Wise Telemetry**:
   - Metropolitan regional zoning (Wards A through F) with risk classifications, PM2.5 levels, temperature, population vulnerability, hospital coverage, and automated alerts.
5. **Citizen Health Reports**:
   - Public health symptom reporting and community database persistence (`POST /api/citizen-reports`).
   - Real-time aggregate statistics for public health surveillance (`GET /api/citizen-reports/stats`).
6. **Hospital Burden Dashboard**:
   - Medical center facility management and bed occupancy tracking (`GET /api/hospital/facilities`).
   - Predictive hospital admission forecasting correlating emergency intake with particulate spikes and thermal heat indices (`GET /api/hospital-burden`).
7. **AI Clinical Health Assistant**:
   - Contextual chat assistant (`POST /api/chat`) returning actionable medical guidance based on real-time city weather telemetry and user vulnerability profiles.

---

## 🛠️ Quick Start

### 1. Run the Backend
You can launch the backend using the included batch script or directly via python:
```bash
# Option A: Double-click or run:
run_backend.bat

# Option B: Run via virtual environment:
cd climate-healthy-backend
set PYTHONPATH=.
.\venv\Scripts\python app.py
```
The server will start on: **`http://localhost:5000`**

### 2. Interactive API Documentation (Swagger)
Visit **`http://localhost:5000/docs`** to test and explore all endpoints interactively in your browser.

---

## 🗄️ Database Configuration

By default, the backend connects using SQLAlchemy with automatic zero-configuration SQLite fallback (`climate_health.db`) so the application works out-of-the-box.

To connect to your local **PostgreSQL** instance:
Edit `.env`:
```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/climate_health_db
```
When provided, the backend will automatically connect to PostgreSQL, create all required tables (`users`, `citizen_reports`, `ward_telemetry`, `hospital_facilities`, `hospital_burden_stats`, `weather_cache`), and seed default telemetry data.
