# decorators.py ------------------------------------------------------------------------------------
#
# Description:
#    This script contains decorators funtions
#
# --------------------------------------------------------------------------------------------------


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
from functools import wraps
# Installed
from flask import request
# Custom
from app.config.settings import Config
from app.responses import MyException


# ==================================================================================================
# Functions
# ==================================================================================================
#
def should_be_authenticated():
    """This function checks if request must be authenticated"""
    if Config.FILE_MANAGER_API_KEY is None:
        return False
    return True


def should_be_authenticated_for_incoming():
    """This function checks if request must be authenticated for incoming requests"""
    # NOTE: Incoming requests consider in this case all but GET method
    if request.method == 'GET':
        return False
    if Config.FILE_MANAGER_AUTH_INCOMING:
        return True
    return False


def should_be_authenticated_for_outgoing():
    """This function checks if request must be authenticated for outgoing requests"""
    # NOTE: Outgoing requests consider in this case only GET method
    if request.method != 'GET':
        return False
    if Config.FILE_MANAGER_AUTH_OUTGOING and request.method == 'GET':
        return True
    return False


def authenticated():
    """This function checks if a user is authenticated"""
    # Check if Auth is enabled
    if not should_be_authenticated():
        return True
    if not should_be_authenticated_for_incoming() and not should_be_authenticated_for_outgoing():
        return True
    # Check if Authorization exist in request's header
    if Config.FILE_MANAGER_API_KEY_HEADER not in request.headers:
        raise MyException.auth_not_found()
    # Get Authorization
    authorization = request.headers[Config.FILE_MANAGER_API_KEY_HEADER]
    # Check Authorization type
    if Config.FILE_MANAGER_API_KEY != authorization:
        raise MyException.unauthorized()
    return True


# ==================================================================================================
# Decorators
# ==================================================================================================
#
def files_required(f):
    """This function extracts the files"""
    @wraps(f)
    def decorated(*args, **kwargs):
        files = request.files.getlist('files[]')
        files = [f for f in files if f.filename != '']
        if len(files) == 0:
            raise MyException.error('No files are given', 500)
        return f(files, *args, **kwargs)
    return decorated


def unique_filename(f):
    """This function checks if a unique filename must be used"""
    @wraps(f)
    def decorated(*args, **kwargs):
        unique_id = request.args.get('unique_id', type=lambda v: v.lower() == 'true')
        return f(unique_id, *args, **kwargs)
    return decorated


def auth_required(f):
    """This function extracts the authorization for the request and validates it"""
    @wraps(f)
    def decorated(*args, **kwargs):
        is_eligible = authenticated()
        return f(*args, **kwargs)
    return decorated
