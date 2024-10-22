from fastapi import APIRouter, HTTPException
from starlette import status as HTTPStatus

import app.service.creature as service
from app.errors import Duplicate, Missing
from app.models.creature import Creature

router = APIRouter(prefix="/creature", tags=["creature"])


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
async def create(creature: Creature):
    try:
        return service.create(creature)
    except Duplicate as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_409_CONFLICT, detail=str(e)) from e


@router.put("")
@router.put("/")
async def replace(creature: Creature):
    try:
        return service.replace(creature)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.patch("")
@router.patch("/", status_code=200)
async def modify(creature: Creature):
    try:
        return service.modify(creature)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete("/{name}")
async def delete(name: str):
    try:
        service.delete(name)
    except Missing as e:
        raise HTTPException(status_code=HTTPStatus.HTTP_404_NOT_FOUND, detail=str(e)) from e
