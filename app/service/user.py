import os
from datetime import datetime, timedelta, timezone

from jose import jwt

from app.models.user import User

if os.getenv("CRYPTID_UNIT_TEST"):
    from app.fake import user as data
else:
    from app.data import user as data

from passlib.context import CryptContext

SECRET_KEY = os.getenv("CRYPTID_SECRET_KEY", "secret")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_jwt_username(token: str) -> str | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            return None
        return username
    except jwt.JWTError: # type: ignore
        return None


def get_current_user(token: str) -> User | None:
    if not (username := get_jwt_username(token)):
        return None
    if user := lookup_user(username):
        return user
    return None


def lookup_user(name: str) -> User | None:
    if user := data.get_one(name):
        return user
    return None


def authenticate_user(name: str, password: str) -> User | None:
    if not (user := lookup_user(name)):
        return None
    return user if verify_password(password, user.hash) else None


def create_access_token(data: dict, expires: timedelta | None = None) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expires or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_all() -> list[User]:
    return data.get_all()


def get_one(name: str) -> User:
    return data.get_one(name)


def create(user: User) -> User:
    return data.create(user)


def modify(name: str, user: User) -> User:
    return data.modify(name, user)


def delete(name: str) -> None:
    data.delete(name)
