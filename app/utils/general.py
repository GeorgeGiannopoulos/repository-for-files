# general.py ---------------------------------------------------------------------------------------
#
# Description:
#    This script contains general funtions
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
import os
import hashlib
import datetime
# Installed
from werkzeug.utils import secure_filename
# Custom
from app.config.settings import Config
from app.responses import MyException


# ==================================================================================================
# Functions
# ==================================================================================================
#
def now():
    """This function returns the current timestamp"""
    return datetime.datetime.utcnow().strftime('%Y%m%dT%H%M%S')


def file_extension(filename: str):
    """This function returns a file's extension"""
    try:
        fn, ext = os.path.basename(filename).split('.')
    except:
        raise MyException.missing_extension()
    return ext


def check_filename(file, patterns=None):
    """This function validates filename"""
    # Check if its file is secure
    try:
        filename = secure_filename(file.filename)
    except:
        raise MyException.unsecure_filename()
    if filename == '':
        raise MyException.invalid_filename()
    # Check the file extension in case a patterns is given as an argument
    if patterns:
        ext = file_extension(filename)
        if ext not in patterns:
            raise MyException.unexpected_extension()
    return filename


def file_to_blob(file):
    """This function reads a file and resets the pointer to the beginning"""
    blob = file.read()
    file.seek(0)  # Reset the file pointer to the beginning
    return blob


def file_size(file):
    """This function returns the file's size"""
    return len(file_to_blob(file))


def file_hash(file):
    """This function returns a hash calculated using the file content"""
    return hashlib.sha256(file_to_blob(file)).hexdigest()


def unique_filename(file, timestamp=False):
    """This function returns a unique filename"""
    return "{}{}.{}".format(file_hash(file), '_' + now() if timestamp else '', file_extension(file.filename))


def filepath(filename):
    """This function returns the file's path"""
    return os.path.join(Config.FILES_DIR, filename)


def file_metadata(file, basename=None):
    """This function returns the file's metadata"""
    try:
        return {
            'name': file.filename,
            'type': file.content_type,
            'size': file_size(file),
            **({'filename': basename} if basename is not None else {}),
        }
    except:
        return None


def store_file(file, unique_id=True):
    """This function stores a file to filesystem"""
    # Generate filename using file hash and timestamp
    filename = unique_filename(file) if unique_id else check_filename(file)
    metadata = file_metadata(file, filename)
    # Write file to filesystem
    file.save(filepath(filename))
    return metadata if metadata else filename


def store_files(files, unique_id=True):
    """This function stores multiple files to filesystem"""
    if len(files) == 0:
        raise MyException.error('No files are given', 500)
    elif len(files) == 1:
        return store_file(files[0], unique_id=unique_id)
    else:
        return [store_file(f, unique_id=unique_id) for f in files]


def remove_file(filename):
    """This function deletes a file if exist"""
    file_location = filepath(filename)
    # Chech if the file exist
    if os.path.exists(file_location):
        os.remove(file_location)
        return True
    return False
