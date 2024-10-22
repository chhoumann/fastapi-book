import app.data.explorer as data
from app.models.explorer import Explorer


def get_all() -> list[Explorer]:
    return data.get_all()


def get_one(name: str) -> Explorer | None:
    return data.get_one(name)


def create(explorer: Explorer) -> Explorer:
    return data.create(explorer)


def replace(explorer: Explorer) -> Explorer:
    return data.replace(explorer)  # type: ignore


def modify(explorer: Explorer) -> Explorer:
    return data.modify(explorer)  # type: ignore


def delete(id: str) -> None:
    return data.delete(id)
