import os

from flask import Flask
from flask_cors import CORS

from . import rest, web


def create_app(test_config=None):
    # create and configure the app
    project_dir = os.path.dirname(os.path.abspath(__file__))
    instance_path = os.path.join(project_dir, 'instance')
    app = Flask(__name__, instance_path=instance_path, instance_relative_config=False)
    CORS(app)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flask.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(rest.bp)
    app.register_blueprint(web.web_bp)

    return app
