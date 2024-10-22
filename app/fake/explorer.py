from app.models.explorer import Explorer

_explorers = [
    Explorer(name="Claude Hande", country="FR", description="Scarce during full moons"),
    Explorer(name="Noah Weiser", country="DE", description="Myopic machete man"),
]


def get_all() -> list[Explorer]:
    return _explorers


def get_one(name: str) -> Explorer | None:
    for _explorer in _explorers:
        if _explorer.name == name:
            return _explorer
    return None


def create(explorer: Explorer) -> Explorer:
    _explorers.append(explorer)
    return explorer


def modify(explorer: Explorer) -> Explorer | None:
    for i, _explorer in enumerate(_explorers):
        if _explorer.name == explorer.name:
            _explorers[i] = explorer
            return explorer
    return None


def replace(explorer: Explorer) -> Explorer | None:
    for i, _explorer in enumerate(_explorers):
        if _explorer.name == explorer.name:
            _explorers[i] = explorer
            return explorer
    return None


def delete(name: str) -> None:
    for i, _explorer in enumerate(_explorers):
        if _explorer.name == name:
            _explorers.pop(i)
            return
    return None
