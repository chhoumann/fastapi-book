from fastapi import APIRouter, HTTPException
from starlette import status as HTTPStatus

import app.service.explorer as service
from app.errors import Duplicate, Missing
from app.models.explorer import Explorer

router = APIRouter(prefix="/explorer", tags=["explorer"])


@router.get("")
@router.get("/")
async def get_all():
    return service.get_all()


@router.get("/{name}")
async def get_one(name: str):
    try:
        return service.get_one(name)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.post("", status_code=201)
@router.post("/", status_code=201)
async def create(explorer: Explorer):
    try:
        return service.create(explorer)
    except Duplicate as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_409_CONFLICT, detail=str(e)) from e


@router.put("")
@router.put("/")
async def replace(explorer: Explorer):
    try:
        return service.replace(explorer)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.patch("")
@router.patch("/", status_code=200)
async def modify(explorer: Explorer):
    try:
        return service.modify(explorer)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete("/{name}")
async def delete(name: str):
    try:
        service.delete(name)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e
