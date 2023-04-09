from flask import Blueprint, jsonify, Response, request
from despensa.controller import Controller
from despensa.classes import Recipe, Aliment

bp = Blueprint('rest', __name__, url_prefix='/rest')


# CRUD Aliments

@bp.route('/aliments', methods=['GET'])
def get_all_aliments() -> Response:
    aliments: list[Aliment] = Controller().get_all_aliments()
    return jsonify(aliments)


@bp.route('/aliments/<aliment_id>', methods=['GET'])
def get_aliment(aliment_id: str) -> Response:
    aliment: Aliment = Controller().get_aliment_by_id(int(aliment_id))
    return jsonify(aliment)


@bp.route('/aliments', methods=['POST'])
def create_aliment() -> Response:
    aliment = Controller().create_aliment_from_json(request.json)
    return jsonify(aliment)


@bp.route('/aliments/<aliment_id>', methods=['PUT'])
def update_aliment(aliment_id: str) -> Response:
    Controller().update_aliment_from_json(int(aliment_id), request.json)
    return jsonify(success=True)


@bp.route('/aliments/<aliment_id>', methods=['DELETE'])
def delete_aliment(aliment_id: int) -> Response:
    Controller().delete_aliment(int(aliment_id))
    return jsonify(success=True)


# CRUD Recipes

@bp.route('/recipes', methods=['GET'])
def get_all_recipes() -> Response:
    recipes: list[Recipe] = Controller().get_recipes_catalog()
    return jsonify(recipes)


@bp.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id: int) -> Response:
    recipe: Recipe = Controller().get_recipe_by_id(int(recipe_id))
    return jsonify(recipe)


@bp.route('/recipes', methods=['POST'])
def create_recipe() -> Response:
    recipe = Controller().create_recipe_from_json(request.json)
    return jsonify(recipe)


@bp.route('/recipes/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id: str) -> Response:
    Controller().update_recipe_from_json(int(recipe_id), request.json)
    return jsonify(success=True)


@bp.route('/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id: int) -> Response:
    Controller().delete_recipe(int(recipe_id))
    return jsonify(success=True)


# Pantry

@bp.route('/pantry', methods=['GET'])
def get_pantry() -> Response:
    pantry = Controller().get_pantry()
    return jsonify(pantry)


@bp.route('/pantry/<name>', methods=['POST'])
def add_to_pantry(name: str) -> Response:
    Controller().insert_aliment_in_pantry(name)
    return jsonify(success=True)


@bp.route('/pantry/<name>', methods=['DELETE'])
def remove_from_pantry(name: str):
    Controller().remove_aliment_in_pantry(name)
    return jsonify(success=True)


# Shopping List

@bp.route('/shopping_list', methods=['GET'])
def get_shopping_list():
    shopping_list = Controller().get_shopping_list()
    return jsonify(shopping_list)


@bp.route('/shopping_list/<item>', methods=['POST'])
def add_to_shopping_list(item: str):
    Controller().insert_item_in_shopping_list(item)
    return jsonify(success=True)


@bp.route('/shopping_list/<item>', methods=['DELETE'])
def remove_from_shopping_list(item: str):
    Controller().remove_item_from_shopping_list(item)
    return jsonify(success=True)
