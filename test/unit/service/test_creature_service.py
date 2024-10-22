import pytest

import app.service.creature as code
from app.errors import Missing
from app.models.creature import Creature

sample = Creature(name="Sammy", description="A human", country="USA", area="New York", aka="Sammy")


def test_create():
    response = code.create(sample)
    assert response == sample


def test_get_exists():
    response = code.get_one("Sammy")
    assert response == sample


def test_get_missing():
    with pytest.raises(Missing):
        code.get_one("boxturtle")
