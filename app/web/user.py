import os
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette import status as HTTPStatus

from app.models.user import User

if os.getenv("CRYPTID_UNIT_TEST"):
    from app.fake import user as service
else:
    from app.service import user as service

from app.errors import Duplicate, Missing

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/user", tags=["user"])

oauth2_dep = OAuth2PasswordBearer(tokenUrl="token")


def unauthed():
    raise HTTPException(
        status_code=HTTPStatus.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.post("/token")
async def create_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    user = service.authenticate_user(form_data.username, form_data.password)
    if not user:
        unauthed()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = service.create_access_token(data={"sub": user.name}, expires=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/token")
def get_access_token(token: str = Depends(oauth2_dep)) -> dict:
    return {"token": token}


@router.get("/")
def get_all() -> list[User]:
    return service.get_all()


@router.get("/{name}")
def get_one(name: str) -> User:
    try:
        return service.get_one(name)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("/", status_code=HTTPStatus.HTTP_201_CREATED)
def create(user: User) -> User:
    try:
        return service.create(user)
    except Duplicate as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_409_CONFLICT, detail=str(e)) from e


@router.patch("/{name}")
def modify(name: str, user: User) -> User:
    try:
        return service.modify(name, user)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete("/{name}")
def delete(name: str) -> None:
    try:
        service.delete(name)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e
