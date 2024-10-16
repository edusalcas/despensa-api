from typing import Union, Tuple

from flask import Blueprint, jsonify, Response, request
from flask_cors import cross_origin

from despensa.controller import Controller
from despensa.classes import Recipe, Aliment
from despensa.interfaces.logger import Logger, LOG_API_REST

bp = Blueprint('rest', __name__, url_prefix='/rest')

logger = Logger(log_file=LOG_API_REST)

# CRUD Aliments

@bp.route('/aliments', methods=['GET'])
def get_all_aliments() -> Response:
    logger.info("(get_all_aliments)")
    aliments: list[Aliment] = Controller().get_all_aliments()
    logger.info(f"(get_all_aliments) Output: Sended {len(aliments)} aliments: {[al.name for al in aliments]}")
    return jsonify(aliments)


@bp.route('/aliments/<aliment_id>', methods=['GET'])
def get_aliment(aliment_id: str) -> Response:
    logger.info(f"(get_aliment) Input: aliment_id={aliment_id}")
    aliment: Aliment = Controller().get_aliment_by_id(int(aliment_id))
    logger.info(f"(get_aliment) Output: {aliment}")
    return jsonify(aliment)


@bp.route('/aliments', methods=['POST'])
def create_aliment() -> Union[Response, tuple[Response, int]]:
    logger.info(f"(create_aliment) Input: json_data={request.json}")
    try:
        aliment = Controller().create_aliment_from_json(request.json)
        logger.info(f"(create_aliment) Output: {aliment}")
        return jsonify(aliment)
    except Exception as e:
        logger.error(f"(create_aliment): {e}")
        return jsonify({'error': str(e)}), 400


@bp.route('/aliments/<aliment_id>', methods=['PUT'])
def update_aliment(aliment_id: str) -> Response:
    logger.info(f"(update_aliment) Input: aliment_id={aliment_id}")
    Controller().update_aliment_from_json(int(aliment_id), request.json)
    logger.info(f"(update_aliment) Output: Success")
    return jsonify(success=True)


@bp.route('/aliments/<aliment_id>', methods=['DELETE'])
def delete_aliment(aliment_id: int) -> Response:
    logger.info(f"(delete_aliment) Input: aliment_id={aliment_id}")
    Controller().delete_aliment(int(aliment_id))
    logger.info(f"(delete_aliment) Output: Success")
    return jsonify(success=True)


# CRUD Recipes

@bp.route('/recipes', methods=['GET'])
def get_all_recipes() -> Response:
    logger.info(f"(get_all_recipes)")
    recipes: list[Recipe] = Controller().get_recipes_catalog()
    logger.info(f"(get_all_recipes) Output: Sended {len(recipes)} recipes: {[re.name for re in recipes]}")
    return jsonify(recipes)


@bp.route('/recipes/<recipe_id>', methods=['GET'])
def get_recipe(recipe_id: int) -> Response:
    logger.info(f"(get_recipe) Input: recipe_id={recipe_id}")
    recipe: Recipe = Controller().get_recipe_by_id(int(recipe_id))
    logger.info(f"(get_recipe) Output: {recipe}")
    return jsonify(recipe)


@bp.route('/recipes', methods=['POST'])
def create_recipe() -> Union[Response, tuple[Response, int]]:
    logger.info(f"(create_recipe) Input: json_data={request.json}")
    try:
        recipe = Controller().create_recipe_from_json(request.json)
        return jsonify(recipe)
    except Exception as e:
        logger.error(f"(create_recipe): {e}")
        return jsonify({'error': str(e)}), 400


@bp.route('/recipes/<recipe_id>', methods=['PUT'])
def update_recipe(recipe_id: str) -> Response:
    logger.info(f"(update_recipe) Input: recipe_id={recipe_id}")
    Controller().update_recipe_from_json(int(recipe_id), request.json)
    logger.info(f"(update_recipe) Output: Success")
    return jsonify(success=True)


@bp.route('/recipes/<recipe_id>', methods=['DELETE'])
def delete_recipe(recipe_id: int) -> Response:
    logger.info(f"(delete_recipe) Input: recipe_id={recipe_id}")
    Controller().delete_recipe(int(recipe_id))
    logger.info(f"(delete_recipe) Output: Success")
    return jsonify(success=True)


# Pantry

@bp.route('/pantry', methods=['GET'])
def get_pantry() -> Response:
    logger.info(f"(get_pantry)")
    pantry = Controller().get_pantry()
    logger.info(f"(get_pantry) Output: Sended {len(pantry)} aliments in pantry: {[al.name for al in pantry]}")
    return jsonify(pantry)


@bp.route('/pantry/<name>', methods=['POST'])
def add_to_pantry(name: str) -> Response:
    logger.info(f"(add_to_pantry) Input: name={name}")
    Controller().insert_aliment_in_pantry(name)
    logger.info(f"(add_to_pantry) Output: Success")
    return jsonify(success=True)


@bp.route('/pantry/<name>', methods=['DELETE'])
def remove_from_pantry(name: str):
    logger.info(f"(remove_from_pantry) Input: name={name}")
    Controller().remove_aliment_in_pantry(name)
    logger.info(f"(remove_from_pantry) Output: Success")
    return jsonify(success=True)


# Shopping List

@bp.route('/shopping_list', methods=['GET'])
def get_shopping_list():
    logger.info(f"(get_shopping_list)")
    shopping_list = Controller().get_shopping_list()
    logger.info(f"(get_shopping_list) Output: Sended {len(shopping_list)} items in shopping_list: {[it.name for it in shopping_list]}")
    return jsonify(shopping_list)


@bp.route('/shopping_list/<item>', methods=['POST'])
def add_to_shopping_list(item: str):
    logger.info(f"(add_to_shopping_list) Input: item={item}")
    Controller().insert_item_in_shopping_list(item)
    logger.info(f"(add_to_shopping_list) Output: Success")
    return jsonify(success=True)


@bp.route('/shopping_list/<item>', methods=['DELETE'])
def remove_from_shopping_list(item: str):
    logger.info(f"(remove_from_shopping_list) Input: item={item}")
    Controller().remove_item_from_shopping_list(item)
    logger.info(f"(remove_from_shopping_list) Output: Success")
    return jsonify(success=True)
