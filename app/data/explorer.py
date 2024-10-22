from app.data.init import IntegrityError, conn, cursor
from app.errors import Duplicate, Missing
from app.models.explorer import Explorer

assert cursor is not None, "Cursor is not initialized"
assert conn is not None, "Connection is not initialized"

cursor.execute(
    """create table if not exists explorer(
name text primary key,
country text,
description text)"""
)


def row_to_model(row: tuple[str, str, str]) -> Explorer:
    name, country, description = row
    return Explorer(name=name, country=country, description=description)


def model_to_dict(model: Explorer) -> dict[str, str]:
    return model.model_dump()


def get_one(name: str) -> Explorer:
    cursor.execute("select * from explorer where name=:name", {"name": name})
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"Explorer {name} not found")


def get_all() -> list[Explorer]:
    cursor.execute("select * from explorer")
    return [row_to_model(row) for row in cursor.fetchall()]


def create(explorer: Explorer) -> Explorer:
    try:
        cursor.execute(
            "insert into explorer (name, country, description) values (:name, :country, :description)",
            model_to_dict(explorer),
        )
    except IntegrityError as e:
        raise Duplicate(f"Explorer {explorer.name} already exists") from e
    conn.commit()
    return get_one(explorer.name)  # type: ignore


def modify(explorer: Explorer) -> Explorer:
    qry = """update explorer
    set country=:country,
    name=:name,
    description=:description
    where name=:name_orig"""
    params = model_to_dict(explorer)
    params["name_orig"] = explorer.name
    _ = cursor.execute(qry, params)
    conn.commit()
    if cursor.rowcount == 1:
        return get_one(explorer.name)  # type: ignore
    else:
        raise Missing(f"Explorer {explorer.name} not found")


def delete(name: str) -> None:
    cursor.execute("delete from explorer where name=:name", {"name": name})
    conn.commit()
    if cursor.rowcount != 1:
        raise Missing(f"Explorer {name} not found")
