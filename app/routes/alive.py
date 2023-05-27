# alive.py -----------------------------------------------------------------------------------------
#
# Description:
#    This script contains all the routes regarding REST-API status (up and running)
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Routes table of contents
# ==================================================================================================
# Search the Routes based on the following patterns (comments)
#
# | Pattern             | URL    | Methods | Comments
# |---------------------|--------|---------|------------------------
# | --- (router 01) --- | /      | GET     | Return a JSON to ensure that the REST-API is alive
# | --- (router 02) --- | /alive | GET     | Return a simple alive page


# ==================================================================================================
# Logging
# ==================================================================================================
#
# Load Logging
from app.app import logging
logger = logging.getLogger(__name__)


# ==================================================================================================
# Imports
# ==================================================================================================
# Build-in
# NOTE: Add here the Build-in modules
# Installed
from flask import Blueprint, render_template, request
# Custom
from app.responses import MyResponse


# ==================================================================================================
# Constants
# ==================================================================================================
#
blueprint = Blueprint('alive', __name__)


# ==================================================================================================
# Main
# ==================================================================================================
#
# --- (router 01) ---
@blueprint.route('/', methods=['GET'])
def index():
    """This function returns OK to ensure the REST-API is up and running"""
    logger.info('Alive request')
    message = 'The REST-API is up and running'
    return MyResponse.success(message, 200).to_response()


# --- (router 02) ---
@blueprint.route('/alive', methods=['GET'])
def alive_server():
    """This function returns a simple alive page"""
    # Alive Server request
    logger.info('Alive Server request')
    base_url = request.host_url if request.host_url != None else '...'
    mode = 'Server'
    message = "is running under"
    return render_template('alive.html', mode=mode, message=message, status=base_url)
