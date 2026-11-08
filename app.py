import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting ClimaCare AI FastAPI backend on http://localhost:5000 ...")
    uvicorn.run("app.main:app", host="0.0.0.0", port=5000, reload=True)
