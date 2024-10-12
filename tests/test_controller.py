# TODO: All
from typing import Generator
import pytest

from despensa.controller import Controller
from despensa.postgres_connector import PostgresConnector
from environment import Environment

Environment().working_is_test()

@pytest.fixture(scope='function')
def controller() -> Generator[Controller, None, None]:
    with PostgresConnector() as connector:
        connector.clear_all_tables()
        connector.create_all_tables()
        connector.generate_sample_data()
    controller = Controller()
    yield controller
    with PostgresConnector() as connector:
        connector.clear_all_tables()

def test_create_controller(controller):
    assert controller is not None

def test_get_all_aliments(controller):
    assert controller.get_all_aliments() != []

def test_get_pantry(controller):
    assert controller.get_pantry() != []

def test_get_recipes_catalog(controller):
    assert controller.get_recipes_catalog() != []

