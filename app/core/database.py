import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

logger = logging.getLogger(__name__)

def create_database_engine():
    # Try PostgreSQL first
    try:
        database_url = settings.DATABASE_URL
        if database_url.startswith("postgresql://"):
            database_url = database_url.replace(
                "postgresql://", "postgresql+psycopg2://", 1
            )

        pg_engine = create_engine(database_url, pool_pre_ping=True)
        # Attempt connection
        with pg_engine.connect():
            logger.info("Successfully connected to PostgreSQL database.")
            print("[DB] Connected to PostgreSQL successfully.")
        return pg_engine
    except Exception as e:
        logger.warning(f"Could not connect to PostgreSQL ({e}). Falling back to local SQLite.")
        print(f"[DB] PostgreSQL unavailable ({e}). Using SQLite fallback: {settings.SQLITE_FALLBACK_URL}")
        return create_engine(
            settings.SQLITE_FALLBACK_URL,
            connect_args={"check_same_thread": False}
        )

engine = create_database_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
