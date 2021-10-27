"""Main module tags_agr project."""
import os

UPLOAD_FOLDER_ADOBE = 'adobe_upload'
UPLOAD_FOLDER_RESIZE = 'resize_upload'
RESULT_FOLDER_RESIZE = 'resize_result'
UPLOAD_FOLDER_LONG = 'long_upload'

if not os.path.isdir(UPLOAD_FOLDER_ADOBE):
    os.mkdir(UPLOAD_FOLDER_ADOBE)

if not os.path.isdir(UPLOAD_FOLDER_RESIZE):
    os.mkdir(UPLOAD_FOLDER_RESIZE)

if not os.path.isdir(RESULT_FOLDER_RESIZE):
    os.mkdir(RESULT_FOLDER_RESIZE)

if not os.path.isdir(UPLOAD_FOLDER_LONG):
    os.mkdir(UPLOAD_FOLDER_LONG)
