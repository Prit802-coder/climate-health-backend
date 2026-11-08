from typing import Optional, Dict
from pydantic import BaseModel, EmailStr

class ConditionsDict(BaseModel):
    asthma: bool = False
    cardiovascular: bool = False
    allergies: bool = False
    copd: bool = False

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    age: Optional[int] = 30
    occupation: Optional[str] = "indoor"
    conditions: Optional[ConditionsDict] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class ProfileUpdate(BaseModel):
    age: Optional[int] = None
    occupation: Optional[str] = None
    conditions: Optional[ConditionsDict] = None

class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    age: int
    occupation: str
    conditions: ConditionsDict

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
