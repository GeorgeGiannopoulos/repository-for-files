# app.py -------------------------------------------------------------------------------------------
#
# Description:
#    This script initialize the flask app
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Logging
# ==================================================================================================
#
# Load/Configure Logging
from app.config.settings import Config
import logging
from logging import config
logging.config.fileConfig(Config.LOGGING_CNF)
logger = logging.getLogger(__name__)


# ==================================================================================================
# Imports
# ==================================================================================================
# Build-in
import os
# Installed
from flask import Flask
# Custom
from app import commands
from app.config.settings import Config, ConfigProdFlask, ConfigDevFlask
from app.extensions import cors
from app.routes import alive, files
from app.responses import MyException


# ==================================================================================================
# Functions
# ==================================================================================================
#
def create_app():
    """Create an application."""

    FILE_MANAGER_EXECUTION_MODE = os.environ.get('FILE_MANAGER_EXECUTION_MODE', 'production')
    config = ConfigProdFlask if FILE_MANAGER_EXECUTION_MODE == 'production' else ConfigDevFlask

    # Flask app
    logger.info('Flask app initialization')
    app = Flask(__name__)
    # Configure app
    logger.info("Execution mode: '{}'".format(FILE_MANAGER_EXECUTION_MODE))
    logger.info("Authentication: {}".format(True if Config.FILE_MANAGER_API_KEY is not None else False))
    logger.info("Lock Incoming: {}".format(Config.FILE_MANAGER_AUTH_INCOMING))
    logger.info("Lock Outgoing: {}".format(Config.FILE_MANAGER_AUTH_OUTGOING))
    app.config.from_object(config)
    # Extensions
    register_extensions(app)
    # Blueprints
    register_blueprints(app)
    # Error Handlers
    register_errorhandlers(app)
    # Commands
    register_commands(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    pass


def register_blueprints(app):
    """Register Flask blueprints"""
    logger.info('Register Flask blueprints')
    # CORS
    origins = app.config.get('CORS_ORIGIN_WHITELIST', '*')
    cors.init_app(alive.blueprint, origins=origins)
    cors.init_app(files.blueprint, origins=origins)
    # Registration
    app.register_blueprint(alive.blueprint)
    app.register_blueprint(files.blueprint)


def register_errorhandlers(app):
    """Register Flask Error Handlers"""
    logger.info('Register Flask Error Handlers')

    def _errorhandler(error):
        return error.to_response()

    app.errorhandler(MyException)(_errorhandler)


def register_commands(app):
    """Register Click Commands"""
    logger.info('Register Flask Commands')
    app.cli.add_command(commands.clean)
    app.cli.add_command(commands.urls)
