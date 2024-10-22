from app.data.init import IntegrityError, conn, cursor
from app.errors import Duplicate, Missing
from app.models.creature import Creature

assert cursor is not None, "Cursor is not initialized"
assert conn is not None, "Connection is not initialized"

cursor.execute(
    """create table if not exists creature(
name text primary key,
description text,
country text,
area text,
aka text)"""
)


def row_to_model(row: tuple[str, str, str, str, str]) -> Creature:
    name, description, country, area, aka = row
    return Creature(
        name=name, description=description, country=country, area=area, aka=aka
    )


def model_to_dict(model: Creature) -> dict[str, str]:
    return model.model_dump()


def get_one(name: str) -> Creature:
    cursor.execute("select * from creature where name=:name", {"name": name})
    row = cursor.fetchone()
    if row:
        return row_to_model(row)
    else:
        raise Missing(f"Creature {name} not found")


def get_all() -> list[Creature]:
    cursor.execute("select * from creature")
    return [row_to_model(row) for row in cursor.fetchall()]


def create(creature: Creature) -> Creature:
    try:
        cursor.execute(
            "insert into creature (name, description, country, area, aka) values (:name, :description, :country, :area, :aka)",
            model_to_dict(creature),
        )
    except IntegrityError as e:
        raise Duplicate(f"Creature {creature.name} already exists") from e
    conn.commit()
    return get_one(creature.name)  # type: ignore


def modify(creature: Creature) -> Creature:
    qry = """update creature
    set country=:country,
    name=:name,
    description=:description,
    area=:area,
    aka=:aka
    where name=:name_orig"""
    params = model_to_dict(creature)
    params["name_orig"] = creature.name
    _ = cursor.execute(qry, params)
    conn.commit()
    if cursor.rowcount == 1:
        return get_one(creature.name)  # type: ignore
    else:
        raise Missing(f"Creature {creature.name} not found")


def delete(name: str) -> None:
    cursor.execute("delete from creature where name=:name", {"name": name})
    conn.commit()
    if cursor.rowcount != 1:
        raise Missing(f"Creature {name} not found")


def replace(creature: Creature) -> Creature:
    delete(creature.name)
    return create(creature)
