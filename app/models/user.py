from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="citizen")
    
    # Biological Risk Profile attributes
    age = Column(Integer, default=32)
    occupation = Column(String(50), default="indoor")  # indoor or outdoor
    has_asthma = Column(Boolean, default=False)
    has_cardiovascular = Column(Boolean, default=False)
    has_allergies = Column(Boolean, default=True)
    has_copd = Column(Boolean, default=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
