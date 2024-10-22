import os

import pytest

from app.errors import Duplicate, Missing
from app.models.creature import Creature

# set this before data imports below for data.init
os.environ["CRYPTID_SQLITE_DB"] = ":memory:"

from app.data import creature


@pytest.fixture
def sample() -> Creature:
    return Creature(
        name="yeti",
        country="CN",
        area="Himalayas",
        description="Harmless Himalayan",
        aka="Abominable Snowman",
    )


def test_create(sample):
    resp = creature.create(sample)
    assert resp == sample


def test_create_duplicate(sample):
    with pytest.raises(Duplicate):
        _ = creature.create(sample)


def test_get_one(sample):
    resp = creature.get_one(sample.name)
    assert resp == sample


def test_get_one_missing():
    with pytest.raises(Missing):
        _ = creature.get_one("boxturtle")


def test_modify(sample):
    sample.area = "Sesame Street"
    resp = creature.modify(sample)
    assert resp == sample


def test_modify_missing():
    thing: Creature = Creature(
        name="snurfle", country="RU", area="", description="some thing", aka=""
    )
    with pytest.raises(Missing):
        _ = creature.modify(thing)


def test_delete(sample):
    resp = creature.delete(sample.name)
    assert resp is None


def test_delete_missing():
    with pytest.raises(Missing):
        _ = creature.delete("boxturtle")
