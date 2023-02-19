import functools
from typing import List

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
from despensa.controller import Controller
from despensa.classes import Recipe

bp = Blueprint('rest', __name__, url_prefix='/rest')


@bp.route('/recipes', methods=['GET'])
def get_recipe():
    recipes: list[Recipe] = Controller().get_recipes_catalog()

    return jsonify(recipes)

def get_recipe():
    recipe = Controller().get_recipe()
