from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, decode_access_token, oauth2_scheme
from app.models.user import User
from app.schemas.auth import UserRegister, UserLogin, UserOut, Token, ProfileUpdate, ConditionsDict

router = APIRouter(prefix="/auth", tags=["Authentication"])

def get_current_user_from_token(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication token required.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_email = payload["sub"]
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    return user

def _user_to_schema(user: User) -> UserOut:
    return UserOut(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role=user.role,
        age=user.age,
        occupation=user.occupation,
        conditions=ConditionsDict(
            asthma=user.has_asthma,
            cardiovascular=user.has_cardiovascular,
            allergies=user.has_allergies,
            copd=user.has_copd
        )
    )

@router.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="An account with this email already exists.")

    hashed_pwd = get_password_hash(user_in.password)
    conds = user_in.conditions or ConditionsDict()

    db_user = User(
        email=user_in.email,
        hashed_password=hashed_pwd,
        full_name=user_in.full_name,
        age=user_in.age or 30,
        occupation=user_in.occupation or "indoor",
        has_asthma=conds.asthma,
        has_cardiovascular=conds.cardiovascular,
        has_allergies=conds.allergies,
        has_copd=conds.copd
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    token = create_access_token(data={"sub": db_user.email, "id": db_user.id})
    return Token(access_token=token, token_type="bearer", user=_user_to_schema(db_user))

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(data={"sub": user.email, "id": user.id})
    return Token(access_token=token, token_type="bearer", user=_user_to_schema(user))

@router.get("/me", response_model=UserOut)
def get_current_user_profile(current_user: User = Depends(get_current_user_from_token)):
    return _user_to_schema(current_user)

@router.put("/profile", response_model=UserOut)
def update_profile(
    profile_in: ProfileUpdate,
    current_user: User = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)
):
    if profile_in.age is not None:
        current_user.age = profile_in.age
    if profile_in.occupation is not None:
        current_user.occupation = profile_in.occupation
    if profile_in.conditions is not None:
        current_user.has_asthma = profile_in.conditions.asthma
        current_user.has_cardiovascular = profile_in.conditions.cardiovascular
        current_user.has_allergies = profile_in.conditions.allergies
        current_user.has_copd = profile_in.conditions.copd

    db.commit()
    db.refresh(current_user)
    return _user_to_schema(current_user)
