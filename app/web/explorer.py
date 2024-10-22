import app.service.explorer as service
from fastapi import APIRouter
from app.models.explorer import Explorer

router = APIRouter(prefix="/explorer", tags=["explorer"])


@router.get("/")
async def get_all():
    return service.get_all()


@router.get("/{name}")
async def get_one(name: str):
    return service.get_one(name)


@router.post("/")
async def create(explorer: Explorer):
    return service.create(explorer)


@router.put("/")
async def replace(explorer: Explorer):
    return service.replace(explorer)


@router.patch("/")
async def modify(explorer: Explorer):
    return service.modify(explorer)


@router.delete("/{name}")
async def delete(name: str):
    return service.delete(name)
