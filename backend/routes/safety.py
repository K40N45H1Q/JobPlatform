from fastapi import APIRouter, Request, HTTPException, Depends, Header
from sqlmodel import Session, select
from hashlib import sha256
from database.models import User, engine
from datetime import datetime, timedelta
import jwt, os, secrets

SECRET_KEY = os.getenv("SECRET_KEY") or secrets.token_hex(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()


def error(key: str, status: int = 400):
    raise HTTPException(
        status_code=status,
        detail={"key": key}
    )


@router.post("/create_account")
async def create_account(request: Request):
    data = await request.json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        error("missing_fields")

    with Session(engine) as session:
        if session.exec(select(User).where(User.username == username)).first():
            error("user_exists")

        user = User(
            username=username,
            account_type=data.get("account_type"),
            hashed_password=sha256(password.encode()).hexdigest()
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        return {"status": "ok", "user_id": user.id}


@router.post("/login")
async def login(request: Request):
    data = await request.json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        error("missing_fields")

    hashed = sha256(password.encode()).hexdigest()

    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()

        if not user or user.hashed_password != hashed:
            error("invalid_credentials")

        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        token = jwt.encode(
            {"user_id": user.id, "exp": expire.timestamp()},
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {"status": "ok", "token": token}


def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        error("unauthorized", 401)

    token = authorization.replace("Bearer ", "")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except:
        error("invalid_token", 401)

    with Session(engine) as session:
        user = session.exec(select(User).where(User.id == user_id)).first()

        if not user:
            error("user_not_found", 401)

        return user


@router.get("/get_me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "username": current_user.username,
        "account_type": current_user.account_type
    }