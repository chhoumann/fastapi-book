from errors import Duplicate, Missing

from app.models.user import User

fakes = [
    User(name="alice", hash="1234567890"),
    User(name="bob", hash="0987654321"),
]


def find(name: str) -> User | None:
    for user in fakes:
        if user.name == name:
            return user
    return None


def check_missing(name: str) -> None:
    if find(name) is None:
        raise Missing(f"user {name} not found")


def check_duplicate(name: str) -> None:
    if find(name) is not None:
        raise Duplicate(f"user {name} already exists")


def get_all() -> list[User]:
    return fakes


def get_one(name: str) -> User:
    check_missing(name)
    return find(name)  # type: ignore


def create(user: User) -> User:
    check_duplicate(user.name)
    fakes.append(user)
    return user


def modify(name: str, user: User) -> User:
    check_missing(name)
    check_duplicate(user.name)
    fake = find(name)  # type: ignore
    fake.name = user.name
    fake.hash = user.hash
    return user


def delete(name: str) -> None:
    check_missing(name)
    fakes.remove(find(name))  # type: ignore
