import app.service.creature as code
from app.models.creature import Creature

sample = Creature(name="Sam", description="A human", country="USA", area="New York", aka="Sammy")


def test_create():
    response = code.create(sample)
    assert response == sample


def test_get_exists():
    code.create(sample)
    response = code.get_one("Sam")
    assert response == sample


def test_get_missing():
    assert code.get_one("boxturtle") is None
