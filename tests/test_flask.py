import pytest
import json

from despensa.classes import Aliment
from despensa.controller import Controller
from despensa_flask import create_app
from environment import Environment


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    Environment().working_is_test()
    # TODO: Add sample data to database
    Controller().generate_db_sample_data()

    yield app

    # TODO: Clean database


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


class TestAliment:
    base_url: str = "/rest/aliments"

    def test_get_all_aliments(self, client):
        response = client.get(self.base_url)
        aliments = Controller().get_all_aliments()
        aliments_flask = json.loads(response.data, object_hook=Aliment.from_json)

        assert aliments == aliments_flask

    def test_get_aliment(self, client):
        db_id: int = 1
        response = client.get(f"{self.base_url}/{db_id}")
        aliment = Controller().get_aliment_by_id(db_id)
        aliment_flask = json.loads(response.data, object_hook=Aliment.from_json)

        assert aliment == aliment_flask

    def test_update_aliment(self, client):
        db_id: int = 1
        client.put(f"{self.base_url}/{db_id}", json={'bd_id': 1, 'name': 'Onion', 'tags': ['vegetable', 'bad']})

        response = client.get(f"{self.base_url}/{db_id}")
        aliment = Controller().get_aliment_by_id(db_id)
        aliment_flask = json.loads(response.data, object_hook=Aliment.from_json)

        assert aliment == aliment_flask

    def test_create_aliment(self, client):
        aliment: Aliment = Aliment(name='Oil', tags=['good', 'healthy'])
        aliments = Controller().get_all_aliments()
        client.post(self.base_url, json={'name': 'Oil', 'tags': ['good', 'healthy'], 'db_id': 0})
        aliments_new = Controller().get_all_aliments()

        assert aliments + [aliment] == aliments_new

    def test_delete_aliment(self, client):
        db_id: int = 1
        aliments = [al for al in Controller().get_all_aliments() if al.db_id != db_id]
        client.delete(f"{self.base_url}/{db_id}")
        aliments_new = Controller().get_all_aliments()

        assert aliments == aliments_new
