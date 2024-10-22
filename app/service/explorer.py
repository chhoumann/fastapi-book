import app.fake.explorer as data
from app.models.explorer import Explorer


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer | None:
    return data.get_one(name)


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def replace(id: int, explorer: Explorer) -> Explorer:
    return data.replace(id, explorer)


def modify(id: int, explorer: Explorer) -> Explorer:
    return data.modify(id, explorer)


def delete(id, explorer: Explorer) -> None:
    return data.delete(id)
