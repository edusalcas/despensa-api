from flask import Blueprint, render_template

web_bp = Blueprint('web', __name__, url_prefix='/')


@web_bp.route('/', methods=['GET'])
def render_index():
    return render_template('index.html')


@web_bp.route('/aliments.html', methods=['GET'])
def render_aliments():
    return render_template('aliments.html')
