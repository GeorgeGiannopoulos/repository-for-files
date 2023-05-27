# files.py -----------------------------------------------------------------------------------------
#
# Description:
#    This script contains all the routes regarding files
#
# --------------------------------------------------------------------------------------------------


# ==================================================================================================
# Routes table of contents
# ==================================================================================================
# Search the Routes based on the following patterns (comments)
#
# | Pattern             | URL                                  | Methods | Comments
# |---------------------|--------------------------------------|---------|--------------------------
# | --- (router 01) --- | /storage/v1/file                     | POST    | Stores a file to filesystem
# | --- (router 02) --- | /storage/v1/file/<filename>          | PUT     | Updates a file to the filesystem
# | --- (router 03) --- | /storage/v1/file/<filename>          | GET     | Returns a file from the filesystem
# | --- (router 04) --- | /storage/v1/file/<filename>          | DELETE  | Deletes a file from the filesystem
# | --- (router 05) --- | /storage/v1/file/donwload/<filename> | GET     | Returns a file from the filesystem as attachment


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
import os
# Installed
from flask import Blueprint, send_file
# Custom
from app.utils.decorators import files_required, unique_filename, auth_required
from app.utils.general import filepath, store_files, remove_file
from app.responses import MyResponse, MyException


# ==================================================================================================
# Constants
# ==================================================================================================
#
blueprint = Blueprint('files', __name__)


# ==================================================================================================
# Main
# ==================================================================================================
#
# --- (router 01) ---
@blueprint.route('/storage/v1/file', methods=['POST'])
@unique_filename
@files_required
@auth_required
def create_file(files: list, unique_id: bool):
    """This function stores a file to the filesystem"""
    logger.info('Request to store file(s)')
    try:
        filename = store_files(files, unique_id)
        return MyResponse.only_data(filename, 200).to_response()
    except Exception as e:
        logger.exception(e)
        raise MyException.error('Failed to store the file!', 500)


# --- (router 02) ---
@blueprint.route('/storage/v1/file/<filename>', methods=['PUT'])
@unique_filename
@files_required
@auth_required
def update_file(files: list, unique_id: bool, filename: str):
    """This function updates a file to the filesystem"""
    logger.info('Request to update file(s)')
    try:
        remove_file(filename)
        filename = store_files(files, unique_id)
        return MyResponse.only_data(filename, 200).to_response()
    except Exception as e:
        logger.exception(e)
        raise MyException.error('Failed to update the file!', 500)


# --- (router 03) ---
@blueprint.route('/storage/v1/file/<filename>', methods=['GET'])
@auth_required
def read_file(filename: str):
    """This function returns a file from the filesystem"""
    logger.info("Request to get file: '{}'".format(filename))
    file_location = filepath(filename)
    if os.path.exists(file_location):
        logger.info("File '{}' retrieved".format(filename))
        return send_file(file_location, download_name=filename)
    else:
        raise MyException.warning("File '{}' not found".format(filename), 404)


# --- (router 04) ---
@blueprint.route("/storage/v1/file/<filename>", methods=['DELETE'])
@auth_required
def delete_file(filename: str):
    """This function deletes a file from the filesystem"""
    logger.info("Request to delete file: '{}'".format(filename))
    if remove_file(filename):
        return MyResponse.success("File '{}' deleted".format(filename), 200).to_response()
    else:
        raise MyException.warning("File '{}' not found".format(filename), 404)


# --- (router 05) ---
@blueprint.route('/storage/v1/file/download/<filename>', methods=['GET'])
@auth_required
def download_file(filename: str):
    """This function returns a file from the filesystem as an attachment"""
    logger.info("Request to download file: '{}'".format(filename))
    file_location = filepath(filename)
    if os.path.exists(file_location):
        logger.info("File '{}' retrieved".format(filename))
        return send_file(file_location, as_attachment=True, download_name=filename)
    else:
        raise MyException.warning("File '{}' not found".format(filename), 404)
