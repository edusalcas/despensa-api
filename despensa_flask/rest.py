from flask import Blueprint, jsonify, Response
from despensa.controller import Controller
from despensa.classes import Recipe, Aliment

bp = Blueprint('rest', __name__, url_prefix='/rest')


@bp.route('/recipes', methods=['GET'])
def get_all_recipes() -> Response:
    recipes: list[Recipe] = Controller().get_recipes_catalog()
    print(recipes)
    return jsonify(recipes)


@bp.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id: int) -> Response:
    recipe: Recipe = Controller().get_recipe_by_id(recipe_id)

    return jsonify(recipe)


@bp.route('/recipes/<recipe_id>', methods=['POST'])
def update_recipe(recipe_id: int) -> Response:
    return jsonify({})


@bp.route('/aliments', methods=['GET'])
def get_all_aliments() -> Response:
    aliments: list[Aliment] = Controller().get_all_aliments()
    print(aliments)
    return jsonify(aliments)


@bp.route('/aliments/<aliment_id>', methods=['GET'])
def get_aliment(aliment_id: int) -> Response:
    aliment: Aliment = Controller().get_aliment_by_id(aliment_id)

    return jsonify(aliment)


@bp.route('/aliments/<aliment_id>', methods=['POST'])
def update_aliment(aliment_id: int) -> Response:
    return jsonify({})
