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
    Controller().delete_aliment(aliment_id)
    return jsonify(success=True)


# CRUD Recipes

@bp.route('/recipes', methods=['GET'])
def get_all_recipes() -> Response:
    recipes: list[Recipe] = Controller().get_recipes_catalog()
    print(recipes)
    return jsonify(recipes)


@bp.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id: int) -> Response:
    recipe: Recipe = Controller().get_recipe_by_id(recipe_id)

    return jsonify(recipe)


@bp.route('/recipes', methods=['POST'])
def update_recipe() -> Response:
    return jsonify({})
