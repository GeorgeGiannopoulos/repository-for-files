# settings.py --------------------------------------------------------------------------------------
#
# Description:
#    This script contains the app's settings
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Imports
# ==================================================================================================
# Build-in
from os import environ, pardir
from os.path import abspath, dirname, join
# Installed
# NOTE: Add here the Installed modules
# Custom
# NOTE: Add here the Custom modules


# ==================================================================================================
# Environmental Variables
# ==================================================================================================
#
# Execution Mode
# NOTE: To control execution mode export the OS environmental variable 'FILE_MANAGER_EXECUTION_MODE' to
#       'development' to use the Development mode [default: 'production']
FILE_MANAGER_EXECUTION_MODE = environ.get('FILE_MANAGER_EXECUTION_MODE', 'production')
# File-Manager port
FILE_MANAGER_PORT = environ.get('FILE_MANAGER_PORT', 8000)
# Authentication
FILE_MANAGER_API_KEY = environ.get('FILE_MANAGER_API_KEY', None)
FILE_MANAGER_AUTH_INCOMING = environ.get('FILE_MANAGER_AUTH_INCOMING', 'True').lower() in ['true', '1', 'yes', 'on']
FILE_MANAGER_AUTH_OUTGOING = not environ.get('FILE_MANAGER_AUTH_OUTGOING', 'False').lower() in ['false', '0', 'no', 'off']
# Set it for CORS
FILE_MANAGER_SERVER_URL = environ.get('FILE_MANAGER_SERVER_URL', None)


# ==================================================================================================
# Functions
# ==================================================================================================
#
def _get_settings(obj):
    """This function returns the dictionary with settings from an object"""
    return {key: getattr(obj, key) for key in dir(obj) if key.isupper()}


# ==================================================================================================
# Classes
# ==================================================================================================
#
class ConfigApp(object):
    """Base Configuration"""
    SETTINGS_DIR = abspath(dirname(__file__))  # This directory
    APP_DIR = abspath(join(SETTINGS_DIR, pardir))
    PROJECT_ROOT = abspath(join(APP_DIR, pardir))
    FILES_DIR = abspath(join(PROJECT_ROOT, 'files'))
    LOGGING_CNF = abspath(join(SETTINGS_DIR, 'logging.conf'))

    FILE_MANAGER_API_KEY_HEADER = 'X-Api-Key'

    FILE_MANAGER_EXECUTION_MODE = FILE_MANAGER_EXECUTION_MODE
    FILE_MANAGER_PORT = FILE_MANAGER_PORT
    FILE_MANAGER_API_KEY = FILE_MANAGER_API_KEY
    FILE_MANAGER_AUTH_INCOMING = FILE_MANAGER_AUTH_INCOMING
    FILE_MANAGER_AUTH_OUTGOING = FILE_MANAGER_AUTH_OUTGOING
    FILE_MANAGER_SERVER_URL = FILE_MANAGER_SERVER_URL


class ConfigFlask(object):
    pass


class ConfigProdFlask(ConfigFlask):
    """Production FastAPI Configuration"""
    ENV = 'prod'
    DEBUG = False
    CORS_ORIGIN_WHITELIST = [
        'http://' + FILE_MANAGER_SERVER_URL,
        'https://' + FILE_MANAGER_SERVER_URL
        # TODO: Add here all the eligible URL that can access the backend
    ] if FILE_MANAGER_SERVER_URL else ['*']


class ConfigDevFlask(ConfigFlask):
    """Developemnt FastAPI Configuration"""
    ENV = 'dev'
    DEBUG = True
    CORS_ORIGIN_WHITELIST = '*'


class Config(ConfigApp):
    """All Configuration"""

    @classmethod
    def get_settings(cls):
        """This function returns object as a dictionary"""
        return _get_settings(cls)
