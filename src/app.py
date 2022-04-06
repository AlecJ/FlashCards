from flask import Flask
from flask_cors import CORS
from src.util import config, loggingFactory
from src.api import api_blueprint
from src.models import db, migrate

_getLogger = loggingFactory('app')


"""
Main app module.

Contains the app factory function.
"""


def create_app():
    logger = _getLogger('create_app')

    # Initialize Flask
    app = Flask(__name__.split(".")[0])

    # Register Blueprints
    app.register_blueprint(api_blueprint)

    # Register db and migrate extensions
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
    db.init_app(app)
    migrate.init_app(app, db)

    # CORS
    CORS(app)

    logger.info('Running environment: {}'.format(config.ENVIRONMENT))
    return app