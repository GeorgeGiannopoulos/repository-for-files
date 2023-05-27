# responses.py -------------------------------------------------------------------------------------
#
# Description:
#    This script contains the parent response classes that will be inherited from other classes
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
# NOTE: Add here the Build-in modules
# Installed
from flask import make_response, jsonify
# Custom
# NOTE: Add here the Custom modules


# ==================================================================================================
# Functions
# ==================================================================================================
#
def template(status='error', message='empty-message', code=500):
    return {'status': status, 'message': message, 'code': code}


# ==================================================================================================
# Constants
# ==================================================================================================
#
# General
MESSING_FIELDS = template('warning', 'Missing fields!', 400)
# Authentication
AUTH_NOT_FOUND = template('warning', 'Auth Not Found!', 401)
UNAUTHORIZED = template('error', 'Unauthorized', 403)


# ==================================================================================================
# Classes
# ==================================================================================================
#
class MyResponse():
    def __init__(self, status, message, code, data=None, header=None, verbose=True):
        self.status = status
        self.message = message
        self.code = code
        self.data = data
        self.header = header
        self.response = {
            'status': self.status,
            'message': self.message,
            **({'data': self.data} if self.data is not None else {})
        }
        self.logger = logger
        self.verbose = verbose

    def log(self):
        if self.logger and self.verbose:
            if self.code < 400:
                self.logger.info(self.message)
            elif 400 <= self.code < 500:
                self.logger.warning(self.message)
            elif 500 <= self.code:
                self.logger.error(self.message)
            else:
                self.logger.debug(self.message)  # <-- Regression case

    def to_json(self):
        if self.header:
            return jsonify(self.response), self.code, self.header
        return jsonify(self.response), self.code

    def to_response(self):
        self.log()
        return make_response(self.to_json())

    @classmethod
    def success(cls, message, code, data=None, verbose=True):
        arg = template('success', message, code)
        arg['verbose'] = verbose
        return cls(**{**arg, 'data': data} if data else {**arg})

    @classmethod
    def warning(cls, message, code, data=None, verbose=True):
        arg = template('warning', message, code)
        arg['verbose'] = verbose
        return cls(**{**arg, 'data': data} if data else {**arg})

    @classmethod
    def error(cls, message, code, data=None, verbose=True):
        arg = template('error', message, code)
        arg['verbose'] = verbose
        return cls(**{**arg, 'data': data} if data else {**arg})

    @classmethod
    def only_data(cls, data, code):
        res = cls(status=None, message=None, code=code, data=data, verbose=False)
        res.response = data
        return res

    #
    # General
    #
    @classmethod
    def missing_fields(cls, data=None):
        return cls(**{**MESSING_FIELDS, 'data': data} if data else {**MESSING_FIELDS})

    #
    # Authentication
    #
    @classmethod
    def auth_not_found(cls):
        return cls(**AUTH_NOT_FOUND, verbose=False)

    @classmethod
    def unauthorized(cls):
        return cls(**UNAUTHORIZED, verbose=False)


class MyException(MyResponse, Exception):
    """Flask catches it and returns it as responce"""

    def __init__(self, **kwargs):
        MyResponse.__init__(self, **kwargs)
        Exception.__init__(self)


class ExtdException(MyResponse, Exception):
    """Extends basic Exception functionality"""

    def __init__(self, **kwargs):
        MyResponse.__init__(self, **kwargs)
        Exception.__init__(self)
