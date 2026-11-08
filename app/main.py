import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base, SessionLocal
from app.routers import auth, weather, health, wards, reports, hospital, chat
from app.routers.wards import seed_wards_if_empty
from app.routers.reports import seed_reports_if_empty
from app.routers.hospital import seed_hospital_if_empty

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("climate-health-backend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables in PostgreSQL (or SQLite fallback) and seed base tables
    logger.info("Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_wards_if_empty(db)
        seed_reports_if_empty(db)
        seed_hospital_if_empty(db)
        logger.info("Database initialized and seeded successfully.")
    except Exception as e:
        logger.error(f"Error during database initialization: {e}")
    finally:
        db.close()
        
    yield
    # Shutdown logic if any

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="2.0.0",
    description="Full-stack FastAPI backend for the ClimaCare Climate Health Advisory System",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount all routers under /api (Standard REST prefix)
app.include_router(auth.router, prefix="/api")
app.include_router(weather.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(wards.router, prefix="/api")
app.include_router(reports.router, prefix="/api")
app.include_router(hospital.router, prefix="/api")
app.include_router(chat.router, prefix="/api")

# Also mount under root (without /api prefix) for backwards compatibility
# with legacy endpoints that call /weather, /hospital-burden, /chat directly
app.include_router(weather.router)
app.include_router(health.router)
app.include_router(wards.router)
app.include_router(reports.router)
app.include_router(hospital.router)
app.include_router(chat.router)

@app.get("/")
def root():
    return {
        "status": "success",
        "service": "ClimaCare AI FastAPI Backend",
        "version": "2.0.0",
        "docs_url": "/docs",
        "message": "ClimaCare AI Backend Running 🚀"
    }

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "service": "climate-health-backend"}
