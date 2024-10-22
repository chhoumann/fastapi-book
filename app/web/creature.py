import fake.creature as service
from fastapi import APIRouter
from model.creature import Creature

router = APIRouter(prefix="/creature", tags=["creature"])


@router.get("/")
async def get_all():
    return service.get_all()


@router.get("/{name}")
async def get_one(name: str):
    return service.get_one(name)


@router.post("/")
async def create(creature: Creature):
    return service.create(creature)


@router.put("/")
async def replace(creature: Creature):
    return service.replace(creature)


@router.patch("/")
async def modify(creature: Creature):
    return service.modify(creature)


@router.delete("/{name}")
async def delete(name: str):
    return service.delete(name)
