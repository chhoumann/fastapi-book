from app.data.init import IntegrityError, conn, cursor
from app.errors import Duplicate, Missing
from app.models.user import User

assert cursor is not None, "cursor is None"
assert conn is not None, "conn is None"

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS users (
    name TEXT PRIMARY KEY,
    hash TEXT NOT NULL
)
"""
)

cursor.execute(
    """
CREATE TABLE IF NOT EXISTS xusers (
    name TEXT PRIMARY KEY,
    hash TEXT NOT NULL
)
"""
)


def row_to_model(row: tuple[str, str]) -> User:
    user, hash = row
    return User(name=user, hash=hash)


def model_to_dict(model: User) -> dict[str, str]:
    return model.model_dump()


def get_one(name: str) -> User:
    cursor.execute("SELECT * FROM users WHERE name = %s", (name,))
    row = cursor.fetchone()
    if row is None:
        raise Missing(f"user {name} not found")
    return row_to_model(row)


def get_all() -> list[User]:
    cursor.execute("SELECT * FROM users")
    return [row_to_model(row) for row in cursor.fetchall()]


def create(user: User, table: str = "users") -> User:
    try:
        cursor.execute(f"INSERT INTO {table} (name, hash) VALUES (%s, %s)", (user.name, user.hash))
    except IntegrityError as e:
        raise Duplicate(f"user {user.name} already exists in {table}") from e
    return user


def modify(name: str, user: User) -> User:
    query = """
    UPDATE users SET name=:name, hash=:hash WHERE name=:name
    """
    cursor.execute(query, {"name0": name, "name": user.name, "hash": user.hash})
    if cursor.rowcount == 1:
        return user
    raise Missing(f"user {name} not found")


def delete(name: str) -> None:
    user = get_one(name)
    query = "delete from user where name = :name"
    cursor.execute(query, {"name": name})
    if cursor.rowcount != 1:
        raise Missing(f"user {name} not found")
    create(user, "xusers")
